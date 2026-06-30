"""Finance tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    facility_id = models.UUIDField()
    patient_id = models.UUIDField(null=True)
    insurer_portion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    out_of_pocket = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ebm_token = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "transactions"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    transaction_id = models.UUIDField()
    method = models.TextField()
    status = models.TextField(default="pending")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider_ref = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "payments"


class Claim(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    transaction_id = models.UUIDField()
    insurer_id = models.UUIDField()
    status = models.TextField(default="submitted")
    reason_code = models.TextField(null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = "claims"
