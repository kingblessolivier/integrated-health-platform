"""Pure CBHI/mutuelle logic (no DB) — unit-tested in tests.py (docs/20)."""


def fund_balance(premiums_total, claims_paid_total) -> float:
    """The mutuelle fund as a live balance: money in (premiums) minus money out (claims paid)."""
    return round(float(premiums_total) - float(claims_paid_total), 2)
