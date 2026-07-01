"""Pure supply-chain logic (no DB) — unit-tested in tests.py (docs/17)."""
from math import ceil


def reorder_quantity(daily_velocity, lead_time_days, safety_stock, on_hand) -> int:
    """Recommended reorder qty = demand over lead time + safety stock - stock on hand.
    Computed from 90-day sales velocity (docs/17). Never negative."""
    target = daily_velocity * lead_time_days + safety_stock
    return max(0, ceil(target - on_hand))
