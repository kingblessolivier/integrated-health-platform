"""Regulatory tables (DDL owned by backend/sql/0003_regulatory_maternity.sql — see docs/48).
National/product-scoped (not tenant-isolated)."""
import uuid

from django.db import models


class DrugRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product_id = models.UUIDField(null=True)
    importer = models.TextField(null=True)
    status = models.TextField(default="registered")
    expires_on = models.DateField(null=True)

    class Meta:
        managed = False
        db_table = "drug_registrations"


class AdverseEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product_id = models.UUIDField(null=True)
    description = models.TextField()
    severity = models.TextField(default="mild")

    class Meta:
        managed = False
        db_table = "adverse_events"
