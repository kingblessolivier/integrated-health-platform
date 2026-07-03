"""
Login issues a JWT carrying the four-axis scope (docs/04, docs/49):
    user_id, tenant_id, geo_scope, max_sensitivity, commands[]

TenantContextMiddleware reads user_id/tenant_id to set the RLS session vars;
HoldsCommand reads `commands` to authorise each request.
"""
from django.db import connection, transaction
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.security.mfa import verify_totp
from apps.security.models import MfaDevice

from .models import Staff, UserCommand


def build_claims(staff: Staff) -> dict:
    """Assemble the four-axis claim set for a Staff member from their command bundle."""
    commands = list(
        UserCommand.objects.filter(staff_id=staff.id).values_list("command", flat=True)
    )
    return {
        "user_id": str(staff.id),
        "tenant_id": str(staff.tenant_id),
        "geo_scope": staff.geo_scope,
        "max_sensitivity": staff.max_sensitivity,
        "commands": commands,
    }


def resolve_login_claims(nida_id: str) -> dict | None:
    """Look up a user's four-axis claims by national ID at login.

    Login happens before any tenant context exists, so `app.tenant_id` is unset and the
    FORCE-RLS `staff` table would hide every row from a plain query — leaving the JWT with no
    commands. The `login_claims` SECURITY DEFINER function (sql/0005) bypasses RLS for this one
    pre-auth read. If it isn't installed (e.g. a test DB, or a superuser dev role where RLS is
    moot), fall back to the ORM.
    """
    try:
        # Savepoint so a missing function under ATOMIC_REQUESTS doesn't poison the request txn.
        with transaction.atomic(), connection.cursor() as cur:
            cur.execute(
                "SELECT staff_id, tenant_id, geo_scope, max_sensitivity, commands "
                "FROM login_claims(%s)",
                [nida_id],
            )
            row = cur.fetchone()
        if not row:
            return None
        return {
            "user_id": str(row[0]),
            "tenant_id": str(row[1]),
            "geo_scope": row[2],
            "max_sensitivity": row[3],
            "commands": list(row[4] or []),
        }
    except Exception:
        # Resolver absent/unavailable — fall back to the ORM (works when RLS is not in play).
        staff = Staff.objects.filter(nida_id=nida_id).first()
        return build_claims(staff) if staff is not None else None


class FourAxisTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """Enforce a second factor before minting tokens for MFA-enrolled users (docs/66 8b).

        Password auth runs first (super().validate); only then do we demand the OTP,
        so a wrong password never reveals whether MFA is enabled. Users without a
        confirmed device are unaffected until they enrol.
        """
        data = super().validate(attrs)
        device = MfaDevice.objects.filter(user=self.user, confirmed=True).first()
        if device is not None:
            otp = (self.initial_data.get("otp") or "").strip()
            if not otp or not verify_totp(device.secret, otp):
                raise AuthenticationFailed(
                    "A valid one-time code is required.", code="mfa_required"
                )
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Map the authenticated account to its Staff row (by national ID == username here).
        # Uses the RLS-bypassing resolver because login precedes any tenant context.
        claims = resolve_login_claims(user.get_username())
        if claims:
            for key, value in claims.items():
                token[key] = value
        return token


class FourAxisTokenView(TokenObtainPairView):
    serializer_class = FourAxisTokenSerializer
