"""
Pure billing logic (no DB) — unit-tested in tests.py.

- split_payment: divide a total between insurer and patient by a covered rate.
- issue_ebm_receipt / momo stubs: placeholders for the RRA EBM and Mobile Money adapters
  (swap for real integrations behind circuit breakers — docs/09, docs/36).
"""
import secrets
from decimal import ROUND_HALF_UP, Decimal


def split_payment(total, covered_rate):
    """Return (insurer_portion, out_of_pocket) for `total` given a 0..1 `covered_rate`.

    Amounts are quantised to 2 decimal places; the patient pays the remainder so the two
    parts always sum exactly to `total`.
    """
    total = Decimal(str(total))
    rate = Decimal(str(covered_rate))
    if total < 0:
        raise ValueError("total must be non-negative")
    if not (Decimal(0) <= rate <= Decimal(1)):
        raise ValueError("covered_rate must be between 0 and 1")
    insurer = (total * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    out_of_pocket = total - insurer
    return insurer, out_of_pocket


def issue_ebm_receipt(_payload=None) -> str:
    """Stub for the RRA EBM 2.0 certification — returns a certification token."""
    return f"EBM-{secrets.token_hex(8).upper()}"


def momo_request_to_pay(_amount, _msisdn=None) -> str:
    """Stub for MTN MoMo / Airtel Money request-to-pay — returns a provider reference."""
    return f"MOMO-{secrets.token_hex(6).upper()}"
