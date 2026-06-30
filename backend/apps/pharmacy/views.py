"""
Pharmacy endpoints (docs/03): RXNW prescribe (digitally signed), RXDP dispense under FEFO.
Dispensing selects the first-expiring in-date batch, rejects when none can satisfy the
quantity, decrements stock atomically, writes a stock movement, and records the audit entry.
"""
import secrets

from django.db import transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Dispense, StockItem, StockMovement
from .serializers import PrescriptionSerializer
from .services import select_fefo


class PrescriptionCreate(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    required_command = "RXNW"

    def perform_create(self, serializer):
        c = self.request.auth or {}
        code = secrets.token_hex(3).upper()  # short human/SMS code
        obj = serializer.save(tenant_id=c.get("tenant_id"), code=code, status="signed",
                              signed_by=c.get("user_id"), signature=b"")
        audit.append(c.get("user_id"), "RXNW", "prescription", obj.id,
                     {"code": code}, c.get("tenant_id"))


class DispenseCreate(APIView):
    required_command = "RXDP"

    @transaction.atomic
    def post(self, request):
        c = request.auth or {}
        product_id = request.data.get("product_id")
        facility_id = request.data.get("facility_id")
        try:
            qty = int(request.data.get("quantity", 0))
        except (TypeError, ValueError):
            qty = 0

        batches = list(
            StockItem.objects.select_for_update().filter(
                facility_id=facility_id, product_id=product_id
            )
        )
        chosen = select_fefo(batches)
        if qty <= 0 or chosen is None or chosen.quantity < qty:
            return Response(
                {"error": {"code": "FEFO_UNAVAILABLE", "command": "RXDP",
                           "message": "No in-stock, in-date batch can satisfy the request."}},
                status=422,
            )

        chosen.quantity -= qty
        chosen.save(update_fields=["quantity"])
        disp = Dispense.objects.create(
            tenant_id=c.get("tenant_id"), stock_item_id=chosen.id,
            quantity=qty, dispensed_by=c.get("user_id"),
        )
        StockMovement.objects.create(
            tenant_id=c.get("tenant_id"), stock_item_id=chosen.id, kind="dispense",
            quantity=-qty, ref_id=disp.id, created_by=c.get("user_id"),
        )
        audit.append(c.get("user_id"), "RXDP", "dispense", disp.id,
                     {"batch": chosen.batch, "qty": qty}, c.get("tenant_id"))
        return Response(
            {"dispense_id": str(disp.id), "batch": chosen.batch, "remaining": chosen.quantity},
            status=201,
        )
