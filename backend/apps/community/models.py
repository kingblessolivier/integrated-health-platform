"""Community-health tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class ChwVisit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    chw_id = models.UUIDField()
    patient_id = models.UUIDField(null=True)
    village_id = models.UUIDField(null=True)
    kind = models.TextField()           # iccm | anc | pnc | fp | tb | ncd
    payload = models.JSONField(default=dict)
    gps_ok = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "chw_visits"


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    patient_id = models.UUIDField()
    from_facility = models.UUIDField(null=True)
    to_facility = models.UUIDField(null=True)
    tracking_code = models.CharField(max_length=6)
    status = models.TextField(default="created")
    context = models.JSONField(default=dict)

    class Meta:
        managed = False
        db_table = "referrals"
