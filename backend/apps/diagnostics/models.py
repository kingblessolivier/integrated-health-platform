"""Lab/imaging tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    encounter_id = models.UUIDField()
    type = models.TextField()          # lab | imaging | medication
    status = models.TextField(default="placed")
    detail = models.JSONField(default=dict)
    created_by = models.UUIDField()

    class Meta:
        managed = False
        db_table = "orders"


class LabResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    order_id = models.UUIDField()
    analyte = models.TextField()
    value = models.TextField()
    unit = models.TextField(null=True)
    signed_by = models.UUIDField(null=True)
    signed_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "lab_results"


class ImagingReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    order_id = models.UUIDField()
    dicom_ref = models.TextField(null=True)
    report = models.TextField(null=True)
    signature = models.BinaryField(null=True)
    signed_by = models.UUIDField(null=True)
    signed_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "imaging_reports"
