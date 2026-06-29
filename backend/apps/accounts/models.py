"""
Access-model tables. The canonical schema (all tables + RLS) is docs/48 /
backend/sql/0001_initial.sql; these ORM models mirror the subset the API layer touches.
`managed = False` so the SQL migration owns the DDL.
"""
import uuid

from django.db import models


class Command(models.Model):
    code = models.CharField(primary_key=True, max_length=4)
    domain = models.CharField(max_length=2)
    action = models.CharField(max_length=2)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = "commands"


class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    tenant_id = models.UUIDField()
    facility_id = models.UUIDField(null=True)
    nida_id = models.TextField(null=True)
    full_name = models.TextField()
    geo_scope = models.JSONField(default=dict)
    max_sensitivity = models.TextField(default="individual")
    status = models.TextField(default="active")

    class Meta:
        managed = False
        db_table = "staff"


class UserCommand(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, db_column="staff_id")
    command = models.ForeignKey(Command, on_delete=models.DO_NOTHING, db_column="command")

    class Meta:
        managed = False
        db_table = "user_commands"
