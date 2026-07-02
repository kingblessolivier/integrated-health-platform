import os

from django.test import override_settings

from apps.security.mfa import totp, verify_totp

_LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_SECRET = "JBSWY3DPEHPK3PXP"  # test-only TOTP secret


@override_settings(CACHES=_LOCMEM)
def test_blacklist_roundtrip():
    from apps.security import blacklist as bl
    assert bl.is_blacklisted("jti-x") is False
    bl.blacklist_jti("jti-x")
    assert bl.is_blacklisted("jti-x") is True


def test_totp_verifies_own_code():
    at = 1_700_000_000
    assert verify_totp(_SECRET, totp(_SECRET, at=at), at=at) is True


def test_totp_rejects_wrong_code():
    assert verify_totp(_SECRET, "000000", at=1_700_000_000) is False


def test_totp_skew_window():
    at = 1_700_000_000
    prev = totp(_SECRET, at=at - 30)
    assert verify_totp(_SECRET, prev, at=at, window=1) is True


def test_phi_encryption_roundtrip():
    from cryptography.fernet import Fernet
    os.environ["PHI_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    from apps.security.crypto import decrypt_phi, encrypt_phi
    token = encrypt_phi("nid-1199900000000001")
    assert token != "nid-1199900000000001"
    assert decrypt_phi(token) == "nid-1199900000000001"


def test_encrypted_field_prep_and_read_roundtrip():
    from cryptography.fernet import Fernet
    os.environ["PHI_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    from apps.security.fields import EncryptedTextField
    field = EncryptedTextField()
    stored = field.get_prep_value("chronic condition note")
    assert stored != "chronic condition note"  # ciphertext at rest
    assert field.from_db_value(stored, None, None) == "chronic condition note"


def test_encrypted_field_passes_through_null_and_empty():
    from apps.security.fields import EncryptedTextField
    field = EncryptedTextField()
    assert field.get_prep_value(None) is None
    assert field.get_prep_value("") == ""
    assert field.from_db_value(None, None, None) is None


def test_encrypted_field_tolerates_legacy_plaintext():
    from cryptography.fernet import Fernet
    os.environ["PHI_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    from apps.security.fields import EncryptedTextField
    field = EncryptedTextField()
    # A value written before encryption was enabled is returned unchanged.
    assert field.from_db_value("legacy plaintext", None, None) == "legacy plaintext"
