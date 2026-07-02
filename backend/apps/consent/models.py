"""Consent table (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class Consent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    patient_id = models.UUIDField()
    actor_scope = models.JSONField(default=dict)   # {"staff_id": "...", "data_category": "..."}
    status = models.TextField(default="granted")   # granted | revoked

    class Meta:
        managed = False
        db_table = "consents"
