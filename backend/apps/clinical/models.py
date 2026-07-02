"""Clinical tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models

from apps.security.fields import EncryptedTextField


class Encounter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    facility_id = models.UUIDField()
    patient_id = models.UUIDField()
    status = models.TextField(default="open")
    encounter_date = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()

    class Meta:
        managed = False
        db_table = "encounters"


class Diagnosis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    encounter_id = models.UUIDField()
    icd_code = models.TextField()
    note = EncryptedTextField(null=True, blank=True)  # PHI: encrypted at rest (docs/66 9a)
    created_by = models.UUIDField()

    class Meta:
        managed = False
        db_table = "diagnoses"
