"""
Community-health endpoints (docs/03, docs/10): CHIC record a CHW visit (idempotent so the
offline op-log can safely replay it), RFNW create a referral with a tracking code (SMS stub),
RFRC receive a referral by code. All audited.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import ChwVisit, Referral
from .serializers import ChwVisitSerializer, ReferralSerializer
from .services import generate_tracking_code


class ChwVisitCreate(generics.CreateAPIView):
    """Record a CHW visit. Honours an `Idempotency-Key` header for safe offline replay."""
    serializer_class = ChwVisitSerializer
    required_command = "CHIC"

    def create(self, request, *args, **kwargs):
        c = request.auth or {}
        key = request.headers.get("Idempotency-Key")
        if key:
            existing = ChwVisit.objects.filter(payload__client_op_id=key).first()
            if existing is not None:  # already applied — replay is a no-op
                return Response(self.get_serializer(existing).data, status=200)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data.get("payload") or {})
        if key:
            payload["client_op_id"] = key
        obj = serializer.save(tenant_id=c.get("tenant_id"), chw_id=c.get("user_id"),
                              payload=payload, gps_ok=bool(request.data.get("gps_ok", True)))
        audit.append(c.get("user_id"), "CHIC", "chw_visit", obj.id,
                     {"kind": obj.kind, "gps_ok": obj.gps_ok}, c.get("tenant_id"))
        return Response(self.get_serializer(obj).data, status=201)


class ReferralCreate(generics.CreateAPIView):
    serializer_class = ReferralSerializer
    required_command = "RFNW"

    def perform_create(self, serializer):
        c = self.request.auth or {}
        code = generate_tracking_code()
        obj = serializer.save(tenant_id=c.get("tenant_id"), tracking_code=code, status="created")
        # SMS dispatch to caregiver is stubbed (Africa's Talking adapter — docs/09).
        audit.append(c.get("user_id"), "RFNW", "referral", obj.id,
                     {"tracking_code": code}, c.get("tenant_id"))


class ReferralByCode(APIView):
    required_command = "RFRC"

    def get(self, request, code):
        ref = Referral.objects.filter(tracking_code=code).first()
        if ref is None:
            return Response(status=404)
        return Response(ReferralSerializer(ref).data)
