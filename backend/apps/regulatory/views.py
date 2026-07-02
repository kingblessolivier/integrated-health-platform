"""
Rwanda FDA endpoints (docs/03): RGDR register a drug, RGPV report an adverse event,
RGRC recall (suspend a registration). Command-bound + audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import AdverseEvent, DrugRegistration


class DrugRegister(APIView):
    required_command = "RGDR"

    def post(self, request):
        c = request.auth or {}
        reg = DrugRegistration.objects.create(
            product_id=request.data.get("product_id"), importer=request.data.get("importer"),
            status="registered", expires_on=request.data.get("expires_on"))
        audit.append(c.get("user_id"), "RGDR", "drug_registration", reg.id, {}, c.get("tenant_id"))
        return Response({"registration_id": str(reg.id), "status": "registered"}, status=201)


class AdverseEventReport(APIView):
    required_command = "RGPV"

    def post(self, request):
        c = request.auth or {}
        event = AdverseEvent.objects.create(
            product_id=request.data.get("product_id"),
            description=request.data.get("description", ""),
            severity=request.data.get("severity", "mild"))
        audit.append(c.get("user_id"), "RGPV", "adverse_event", event.id,
                     {"severity": event.severity}, c.get("tenant_id"))
        return Response({"event_id": str(event.id)}, status=201)


class Recall(APIView):
    required_command = "RGRC"

    def post(self, request, registration_id):
        c = request.auth or {}
        updated = DrugRegistration.objects.filter(id=registration_id).update(status="recalled")
        if not updated:
            return Response(status=404)
        audit.append(c.get("user_id"), "RGRC", "drug_registration", registration_id, {},
                     c.get("tenant_id"))
        return Response({"registration_id": str(registration_id), "status": "recalled"})
