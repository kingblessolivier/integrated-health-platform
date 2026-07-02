"""
Transparent PHI field encryption (docs/08, docs/66 gap 9a). An EncryptedTextField
encrypts on write and decrypts on read via apps.security.crypto (Fernet), so the
ciphertext is what lands at rest in the column. Reads tolerate NULL and legacy
plaintext, letting an existing column be migrated in place without a rewrite.
"""
from django.db import models

from .crypto import decrypt_phi, encrypt_phi


class EncryptedTextField(models.TextField):
    """A TextField whose value is Fernet-encrypted at rest."""

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None or value == "":
            return value
        return encrypt_phi(value)

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return value
        try:
            return decrypt_phi(value)
        except Exception:
            # Legacy plaintext written before encryption was enabled — return as-is.
            return value
