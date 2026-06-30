"""Pure pharmacy logic (no DB) — unit-tested in tests.py."""
from datetime import date


def select_fefo(items, today=None):
    """First-Expiring, First-Out batch selection.

    Returns the in-stock (`quantity > 0`), non-expired (`expiry_date >= today`) batch
    with the **earliest** expiry, or None if nothing is eligible. `items` are any objects
    exposing `expiry_date` (date) and `quantity` (int).
    """
    today = today or date.today()
    eligible = [i for i in items if i.quantity > 0 and i.expiry_date >= today]
    return min(eligible, key=lambda i: i.expiry_date, default=None)
