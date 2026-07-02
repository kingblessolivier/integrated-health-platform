"""
B2B supply-chain endpoints (docs/03, docs/17): SCRO reorder recommendation (from sales
velocity), SCPO create purchase order, SCRV receive/verify. Command-bound + audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import PurchaseOrder
from .services import reorder_quantity


class ReorderRecommendation(APIView):
    required_command = "SCRO"

    def post(self, request):
        try:
            qty = reorder_quantity(
                float(request.data.get("daily_velocity", 0)),
                float(request.data.get("lead_time_days", 0)),
                float(request.data.get("safety_stock", 0)),
                float(request.data.get("on_hand", 0)))
        except (TypeError, ValueError):
            return Response({"error": {"code": "INVALID_INPUT", "command": "SCRO"}}, status=422)
        return Response({"reorder_quantity": qty})


class PurchaseOrderCreate(APIView):
    required_command = "SCPO"

    def post(self, request):
        c = request.auth or {}
        po = PurchaseOrder.objects.create(
            tenant_id=c.get("tenant_id"), facility_id=request.data.get("facility_id"),
            supplier_id=request.data.get("supplier_id"), status="sent",
            total=request.data.get("total", 0))
        audit.append(c.get("user_id"), "SCPO", "purchase_order", po.id,
                     {"total": str(po.total)}, c.get("tenant_id"))
        return Response({"po_id": str(po.id), "status": "sent"}, status=201)


class GoodsReceiveVerify(APIView):
    required_command = "SCRV"

    def post(self, request, po_id):
        c = request.auth or {}
        updated = PurchaseOrder.objects.filter(id=po_id).update(status="received")
        if not updated:
            return Response(status=404)
        audit.append(c.get("user_id"), "SCRV", "purchase_order", po_id, {}, c.get("tenant_id"))
        return Response({"po_id": str(po_id), "status": "received"})
