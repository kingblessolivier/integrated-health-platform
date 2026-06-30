"""Pharmacy/inventory tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class StockItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    facility_id = models.UUIDField()
    product_id = models.UUIDField()
    batch = models.TextField()
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    shelf = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "stock_items"


class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    encounter_id = models.UUIDField()
    code = models.TextField()
    status = models.TextField(default="signed")
    signed_by = models.UUIDField()
    signature = models.BinaryField()

    class Meta:
        managed = False
        db_table = "prescriptions"


class Dispense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    prescription_item_id = models.UUIDField(null=True)
    stock_item_id = models.UUIDField()
    quantity = models.IntegerField()
    dispensed_by = models.UUIDField()

    class Meta:
        managed = False
        db_table = "dispenses"


class StockMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    stock_item_id = models.UUIDField()
    kind = models.TextField()
    quantity = models.IntegerField()
    ref_id = models.UUIDField(null=True)
    created_by = models.UUIDField(null=True)

    class Meta:
        managed = False
        db_table = "stock_movements"
