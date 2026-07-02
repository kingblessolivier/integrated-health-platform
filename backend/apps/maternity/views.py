"""
Maternity endpoints (docs/03): MTDL record delivery, MTBR register birth (feeds civil
registration; flags birth weight). Command-bound, RLS-scoped, audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Birth, Delivery
from .services import classify_birth_weight


class DeliveryRecord(APIView):
    required_command = "MTDL"

    def post(self, request):
        c = request.auth or {}
        delivery = Delivery.objects.create(
            tenant_id=c.get("tenant_id"), encounter_id=request.data.get("encounter_id"),
            patient_id=request.data.get("patient_id"),
            outcome=request.data.get("outcome", "live_birth"))
        audit.append(c.get("user_id"), "MTDL", "delivery", delivery.id, {}, c.get("tenant_id"))
        return Response({"delivery_id": str(delivery.id)}, status=201)


class BirthRegister(APIView):
    required_command = "MTBR"

    def post(self, request):
        c = request.auth or {}
        weight = request.data.get("weight_grams")
        birth = Birth.objects.create(
            tenant_id=c.get("tenant_id"), delivery_id=request.data.get("delivery_id"),
            sex=request.data.get("sex"), weight_grams=weight, registered=True)
        flag = classify_birth_weight(weight)
        audit.append(c.get("user_id"), "MTBR", "birth", birth.id, {"weight_flag": flag},
                     c.get("tenant_id"))
        return Response({"birth_id": str(birth.id), "registered": True, "weight_flag": flag},
                        status=201)
