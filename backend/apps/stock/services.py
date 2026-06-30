"""Pure stock logic (no DB) — unit-tested in tests.py. Expiry bucketing (90/60/30) and
low-stock detection per docs/16."""


def expiry_bucket(expiry_date, today) -> str:
    """Bucket a batch by days to expiry: expired | 30 | 60 | 90 | ok."""
    days = (expiry_date - today).days
    if days < 0:
        return "expired"
    if days <= 30:
        return "30"
    if days <= 60:
        return "60"
    if days <= 90:
        return "90"
    return "ok"


def is_low_stock(quantity, threshold=10) -> bool:
    return quantity < threshold
