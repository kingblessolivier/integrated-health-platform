"""Maternity tables (DDL owned by backend/sql/0003_regulatory_maternity.sql — see docs/48)."""
import uuid

from django.db import models


class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    encounter_id = models.UUIDField(null=True)
    patient_id = models.UUIDField(null=True)
    outcome = models.TextField(default="live_birth")

    class Meta:
        managed = False
        db_table = "deliveries"


class Birth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    delivery_id = models.UUIDField()
    sex = models.TextField(null=True)
    weight_grams = models.IntegerField(null=True)
    registered = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "births"
