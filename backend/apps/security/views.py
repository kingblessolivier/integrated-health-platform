"""
Security endpoints:
- SELK LOCK (docs/03, docs/16) — terminate a compromised session by blacklisting its
  JWT id. Command-bound + audited.
- MFA enrolment (docs/08, docs/04 tier 2) — any authenticated user can enrol a TOTP
  device and confirm it; no command needed. Login enforces the confirmed device
  (apps/accounts/tokens.py).
- MFA reset (SEMR) — an administrator clears a user's device so they can re-enrol
  (e.g. lost phone). Command-bound + audited.
"""
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Staff
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


class MfaReset(APIView):
    """Admin action (SEMR): clear a target user's TOTP device by their national ID, so they
    can re-enrol after e.g. losing their phone. Removing the device also lifts login
    enforcement for that user until they enrol again. The reset is audited against the target
    Staff id (never the secret)."""

    required_command = "SEMR"

    def post(self, request):
        c = request.auth or {}
        nida_id = str(request.data.get("nida_id") or "").strip()
        if not nida_id:
            return Response({"detail": "nida_id is required."}, status=400)
        # The auth username is the national ID (see FourAxisTokenSerializer.get_token).
        user = User.objects.filter(username=nida_id).first()
        deleted = 0
        if user is not None:
            deleted, _ = MfaDevice.objects.filter(user=user).delete()
        target_staff = Staff.objects.filter(nida_id=nida_id).values_list("id", flat=True).first()
        audit.append(c.get("user_id"), "SEMR", "mfa_device",
                     str(target_staff) if target_staff else None,
                     {"nida_id": nida_id, "cleared": bool(deleted)}, c.get("tenant_id"))
        if not deleted:
            return Response({"detail": "No MFA device found for that user."}, status=404)
        return Response({"status": "reset", "nida_id": nida_id})
