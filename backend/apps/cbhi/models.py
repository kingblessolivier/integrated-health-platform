"""CBHI tables (DDL owned by backend/sql/0002_domain_extensions.sql — see docs/48)."""
import uuid

from django.db import models


class CbhiMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    patient_id = models.UUIDField(null=True)
    scheme = models.TextField(default="mutuelle")
    status = models.TextField(default="active")

    class Meta:
        managed = False
        db_table = "cbhi_members"


class CbhiPremium(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    member_id = models.UUIDField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "cbhi_premiums"
