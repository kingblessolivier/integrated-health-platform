"""
Application-layer PHI field encryption (docs/08 — AES-256; PHI fields get an extra layer
before write). Uses Fernet (AES-128-CBC + HMAC) with a key from the KMS/HSM-provided
`PHI_ENCRYPTION_KEY`; swap to an envelope-encryption KMS client in production.
"""
import os

from cryptography.fernet import Fernet


def _fernet() -> Fernet:
    key = os.environ.get("PHI_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("PHI_ENCRYPTION_KEY is not set")
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_phi(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_phi(token: str) -> str:
    return _fernet().decrypt(token.encode()).decode()
