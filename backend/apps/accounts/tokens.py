"""
Login issues a JWT carrying the four-axis scope (docs/04, docs/49):
    user_id, tenant_id, geo_scope, max_sensitivity, commands[]

TenantContextMiddleware reads user_id/tenant_id to set the RLS session vars;
HoldsCommand reads `commands` to authorise each request.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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


class FourAxisTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Map the authenticated account to its Staff row (by national ID == username here).
        staff = Staff.objects.filter(nida_id=user.get_username()).first()
        if staff is not None:
            for key, value in build_claims(staff).items():
                token[key] = value
        return token


class FourAxisTokenView(TokenObtainPairView):
    serializer_class = FourAxisTokenSerializer
