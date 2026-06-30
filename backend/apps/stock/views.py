"""
Stock/inventory endpoints (docs/03, docs/16): STIN inquiry, STRC receive goods (batch/expiry),
STEX expiry monitoring (90/60/30 buckets). Reuses the pharmacy StockItem/StockMovement models.
Command-bound, RLS-scoped, audited on writes.
"""
from datetime import date

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit
from apps.pharmacy.models import StockItem, StockMovement

from .services import expiry_bucket, is_low_stock


class StockInquiry(APIView):
    required_command = "STIN"

    def get(self, request):
        qs = StockItem.objects.all()
        facility = request.query_params.get("facility_id")
        if facility:
            qs = qs.filter(facility_id=facility)
        items = [{"id": str(s.id), "product_id": str(s.product_id), "batch": s.batch,
                  "expiry_date": s.expiry_date, "quantity": s.quantity,
                  "low": is_low_stock(s.quantity)} for s in qs[:500]]
        return Response({"items": items})


class ReceiveGoods(APIView):
    required_command = "STRC"

    def post(self, request):
        c = request.auth or {}
        item = StockItem.objects.create(
            tenant_id=c.get("tenant_id"), facility_id=request.data.get("facility_id"),
            product_id=request.data.get("product_id"), batch=request.data.get("batch", ""),
            expiry_date=request.data.get("expiry_date"),
            quantity=int(request.data.get("quantity", 0)))
        StockMovement.objects.create(tenant_id=c.get("tenant_id"), stock_item_id=item.id,
                                     kind="receive", quantity=item.quantity,
                                     created_by=c.get("user_id"))
        audit.append(c.get("user_id"), "STRC", "stock_item", item.id,
                     {"batch": item.batch, "qty": item.quantity}, c.get("tenant_id"))
        return Response({"stock_item_id": str(item.id)}, status=201)


class ExpiryMonitor(APIView):
    required_command = "STEX"

    def get(self, request):
        today = date.today()
        qs = StockItem.objects.all()
        facility = request.query_params.get("facility_id")
        if facility:
            qs = qs.filter(facility_id=facility)
        buckets = {"expired": [], "30": [], "60": [], "90": []}
        for s in qs[:1000]:
            b = expiry_bucket(s.expiry_date, today)
            if b in buckets:
                buckets[b].append({"id": str(s.id), "batch": s.batch,
                                   "expiry_date": s.expiry_date, "quantity": s.quantity})
        return Response({"buckets": buckets})
