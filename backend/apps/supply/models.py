"""Supply-chain tables (DDL owned by backend/sql/0002_domain_extensions.sql — see docs/48)."""
import uuid

from django.db import models


class PurchaseOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    facility_id = models.UUIDField(null=True)
    supplier_id = models.UUIDField(null=True)
    status = models.TextField(default="draft")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = "purchase_orders"


class PurchaseOrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    po_id = models.UUIDField()
    product_id = models.UUIDField(null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = "purchase_order_lines"
