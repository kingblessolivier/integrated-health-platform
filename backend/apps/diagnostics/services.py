"""Pure diagnostics logic (no DB) — unit-tested in tests.py."""


def classify_result(value, ref_low=None, ref_high=None) -> str:
    """Classify a lab value against its reference interval: low | normal | high | unknown.
    Used at result sign-off (docs/12) to flag out-of-range results."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if ref_low is not None and v < float(ref_low):
        return "low"
    if ref_high is not None and v > float(ref_high):
        return "high"
    return "normal"
