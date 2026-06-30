"""
Emergency endpoints (docs/03, docs/19): EMIN intake (912 / SOS / transfer) creates a
dispatch; EMDS assigns the nearest available unit; EMHO handover marks arrival. All audited.
SOS/GPS handling and PostGIS proximity are stubbed/in-process here (see services.py).
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Dispatch
from .services import Unit, nearest_unit


class SosIntake(APIView):
    required_command = "EMIN"

    def post(self, request):
        c = request.auth or {}
        dispatch = Dispatch.objects.create(
            tenant_id=c.get("tenant_id"), patient_id=request.data.get("patient_id"),
            status="requested",
        )
        audit.append(c.get("user_id"), "EMIN", "dispatch", dispatch.id,
                     {"source": request.data.get("source", "sos")}, c.get("tenant_id"))
        return Response({"dispatch_id": str(dispatch.id), "status": "requested"}, status=201)


class DispatchNearest(APIView):
    """Assign the nearest available unit. `candidates` carries the available ambulances'
    positions (from the PostGIS query in production); the ranker picks the closest."""
    required_command = "EMDS"

    def post(self, request, dispatch_id):
        c = request.auth or {}
        origin = request.data.get("origin") or {}
        try:
            origin_pt = (float(origin["lng"]), float(origin["lat"]))
            units = [Unit(id=str(u["id"]), lng=float(u["lng"]), lat=float(u["lat"]))
                     for u in request.data.get("candidates", [])]
        except (KeyError, TypeError, ValueError):
            return Response({"error": {"code": "BAD_GEO", "command": "EMDS"}}, status=422)

        chosen = nearest_unit(origin_pt, units)
        if chosen is None:
            return Response({"error": {"code": "NO_UNIT_AVAILABLE", "command": "EMDS"}},
                            status=422)

        updated = Dispatch.objects.filter(id=dispatch_id).update(
            ambulance_id=chosen.id, status="dispatched")
        if not updated:
            return Response(status=404)
        audit.append(c.get("user_id"), "EMDS", "dispatch", dispatch_id,
                     {"ambulance_id": chosen.id}, c.get("tenant_id"))
        return Response({"dispatch_id": str(dispatch_id), "ambulance_id": chosen.id,
                         "status": "dispatched"})


class Handover(APIView):
    required_command = "EMHO"

    def post(self, request, dispatch_id):
        c = request.auth or {}
        updated = Dispatch.objects.filter(id=dispatch_id).update(
            status="at_hospital", dest_facility=request.data.get("facility_id"))
        if not updated:
            return Response(status=404)
        # The pre-hospital record flows into the hospital EMR (encounter) — wired in the
        # clinical handover step; audited here.
        audit.append(c.get("user_id"), "EMHO", "dispatch", dispatch_id, {}, c.get("tenant_id"))
        return Response({"dispatch_id": str(dispatch_id), "status": "at_hospital"})
