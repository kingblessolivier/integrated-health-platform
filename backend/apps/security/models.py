"""
Security tables (DDL owned by backend/sql/0004_security.sql — see docs/08, docs/66).
`managed = False`: the raw-SQL migration owns the schema, matching the rest of the codebase.
"""
import uuid

from django.contrib.auth.models import User
from django.db import models


class MfaDevice(models.Model):
    """A user's TOTP enrolment. `confirmed` gates login enforcement (docs/66 gap 8b)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="user_id")
    secret = models.TextField()
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "mfa_devices"
