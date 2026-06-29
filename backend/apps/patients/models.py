import uuid

from django.db import models


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    nida_id = models.TextField(null=True, blank=True)
    is_temporary = models.BooleanField(default=False)
    given_name = models.TextField(null=True, blank=True)
    family_name = models.TextField(null=True, blank=True)
    sex = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        managed = False  # DDL owned by backend/sql/0001_initial.sql (docs/48)
        db_table = "patients"
