"""Emergency/ambulance tables (DDL owned by backend/sql/0001_initial.sql — see docs/48).

`last_geom` / `origin_geom` are PostGIS geometry columns; they're read/written via raw SQL
or GeoDjango in production and are intentionally not mapped as ORM fields here.
"""
import uuid

from django.db import models


class Ambulance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    plate = models.TextField()
    type = models.TextField()            # bls | als
    status = models.TextField(default="available")

    class Meta:
        managed = False
        db_table = "ambulances"


class Dispatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    ambulance_id = models.UUIDField(null=True)
    patient_id = models.UUIDField(null=True)
    dest_facility = models.UUIDField(null=True)
    status = models.TextField(default="requested")

    class Meta:
        managed = False
        db_table = "dispatches"
