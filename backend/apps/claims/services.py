"""
Pure claims-pipeline logic (no DB) — unit-tested in tests.py.

- advance: the claim state machine (docs/59). Raises on an invalid transition.
- scrub: the AI claims-scrubbing stub (docs/12). Cross-checks the claim and returns
  (passed, reason_code). Replace the rule set with the real scrubbing/fraud engine later.
"""
from decimal import Decimal

# (status, event) -> next status
_TRANSITIONS = {
    ("submitted", "scrub_start"): "scrubbing",
    ("scrubbing", "scrub_pass"): "approved",
    ("scrubbing", "scrub_flag"): "disputed",
    ("disputed", "review_accept"): "approved",
    ("disputed", "review_reject"): "rejected",
    ("approved", "settle"): "paid",
}


def advance(status: str, event: str) -> str:
    """Return the next claim status for `event`, or raise ValueError if not allowed."""
    try:
        return _TRANSITIONS[(status, event)]
    except KeyError:
        raise ValueError(f"invalid transition: {status} -/-> ({event})") from None


def scrub(amount, has_diagnosis: bool, billed_matches: bool, high_amount_threshold="1000000"):
    """AI-scrubbing stub. Returns (passed: bool, reason_code: str | None).

    Cross-references the claim the way the engine will: positive amount, a backing diagnosis,
    and the billed amount matching the dispensed/priced lines; very large amounts are routed
    to human review rather than auto-approved.
    """
    amount = Decimal(str(amount))
    if amount <= 0:
        return False, "INVALID_AMOUNT"
    if not has_diagnosis:
        return False, "NO_DIAGNOSIS"
    if not billed_matches:
        return False, "AMOUNT_MISMATCH"
    if amount > Decimal(str(high_amount_threshold)):
        return False, "HIGH_AMOUNT_REVIEW"
    return True, None
