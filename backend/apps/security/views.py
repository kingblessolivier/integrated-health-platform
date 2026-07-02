"""
Security endpoints:
- SELK LOCK (docs/03, docs/16) — terminate a compromised session by blacklisting its
  JWT id. Command-bound + audited.
- MFA enrolment (docs/08, docs/04 tier 2) — any authenticated user can enrol a TOTP
  device and confirm it; no command needed. Login enforces the confirmed device
  (apps/accounts/tokens.py).
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .blacklist import blacklist_jti
from .mfa import generate_secret, provisioning_uri, verify_totp
from .models import MfaDevice


class Lock(APIView):
    required_command = "SELK"

    def post(self, request):
        c = request.auth or {}
        jti = request.data.get("jti")
        if jti:
            blacklist_jti(jti)
        audit.append(c.get("user_id"), "SELK", "session", None, {"jti": jti},
                     c.get("tenant_id"))
        return Response({"status": "locked", "jti": jti})


class MfaEnrol(APIView):
    """Start TOTP enrolment for the caller: mint a secret, return it with the otpauth URI
    (client renders the QR). The device stays unconfirmed — and login unaffected — until
    the user proves a code via MfaConfirm. Tier 2: no required_command."""

    def post(self, request):
        c = request.auth or {}
        if MfaDevice.objects.filter(user=request.user, confirmed=True).exists():
            # Replacing a confirmed device is an admin reset, not self-service — otherwise a
            # hijacked session could swap in the attacker's secret.
            return Response(
                {"detail": "MFA already enrolled. Ask an administrator to reset it."},
                status=409,
            )
        secret = generate_secret()
        MfaDevice.objects.update_or_create(
            user=request.user, defaults={"secret": secret, "confirmed": False}
        )
        audit.append(c.get("user_id"), "MFAE", "mfa_device", None, {}, c.get("tenant_id"))
        return Response({
            "secret": secret,
            "otpauth_uri": provisioning_uri(secret, request.user.get_username()),
        })


class MfaConfirm(APIView):
    """Prove possession of the enrolled authenticator: a valid code flips the device to
    confirmed, from which point login demands an OTP. Tier 2: no required_command."""

    def post(self, request):
        c = request.auth or {}
        device = MfaDevice.objects.filter(user=request.user, confirmed=False).first()
        if device is None:
            return Response({"detail": "No pending enrolment."}, status=404)
        otp = str(request.data.get("otp") or "").strip()
        if not otp or not verify_totp(device.secret, otp):
            return Response({"detail": "Invalid code."}, status=400)
        device.confirmed = True
        device.save(update_fields=["confirmed"])
        audit.append(c.get("user_id"), "MFAC", "mfa_device", str(device.id), {},
                     c.get("tenant_id"))
        return Response({"status": "confirmed"})
