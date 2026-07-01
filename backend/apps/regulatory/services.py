"""Pure regulatory logic (no DB) — unit-tested in tests.py (docs/08 regulator role)."""


def registration_status(expires_on, today) -> str:
    """valid | expiring (<=90 days) | expired — for drug-registration monitoring."""
    if expires_on is None:
        return "valid"
    days = (expires_on - today).days
    if days < 0:
        return "expired"
    if days <= 90:
        return "expiring"
    return "valid"
