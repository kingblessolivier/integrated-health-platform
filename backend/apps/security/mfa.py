"""
TOTP MFA (docs/08 — MFA required for clinical/admin roles). Pure stdlib (RFC 6238),
unit-tested — no third-party dependency.
"""
import base64
import hashlib
import hmac
import secrets
import struct
import time
from urllib.parse import quote


def _hotp(secret_b32: str, counter: int, digits: int = 6) -> str:
    pad = "=" * ((8 - len(secret_b32) % 8) % 8)
    key = base64.b32decode(secret_b32.upper() + pad)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)


def totp(secret_b32: str, at: float | None = None, step: int = 30) -> str:
    at = time.time() if at is None else at
    return _hotp(secret_b32, int(at // step))


def verify_totp(secret_b32: str, code: str, at: float | None = None,
                step: int = 30, window: int = 1) -> bool:
    """Verify `code`, tolerating +/- `window` steps of clock skew."""
    at = time.time() if at is None else at
    counter = int(at // step)
    return any(_hotp(secret_b32, counter + i) == str(code).zfill(6)
               for i in range(-window, window + 1))


def generate_secret(nbytes: int = 20) -> str:
    """Random base32 TOTP secret — 20 bytes = 160 bits (RFC 4226 §4 recommends ≥128)."""
    return base64.b32encode(secrets.token_bytes(nbytes)).decode().rstrip("=")


def provisioning_uri(secret_b32: str, account: str, issuer: str = "INHP") -> str:
    """otpauth:// URI for authenticator apps (rendered as a QR by the client)."""
    return (
        f"otpauth://totp/{quote(issuer)}:{quote(account)}"
        f"?secret={secret_b32}&issuer={quote(issuer)}&algorithm=SHA1&digits=6&period=30"
    )
