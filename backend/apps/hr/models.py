"""HR tables (DDL owned by backend/sql/0001_initial.sql — see docs/48)."""
import uuid

from django.db import models


class Licence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    staff_id = models.UUIDField()
    council = models.TextField()
    number = models.TextField()
    expires_on = models.DateField()

    class Meta:
        managed = False
        db_table = "licences"
