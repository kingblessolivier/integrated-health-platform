"""Pure maternity logic (no DB) — unit-tested in tests.py (docs/10)."""


def classify_birth_weight(grams) -> str:
    """low (<2500 g) | normal | macrosomia (>4000 g) | unknown — flags newborns needing care."""
    try:
        g = float(grams)
    except (TypeError, ValueError):
        return "unknown"
    if g <= 0:
        return "unknown"
    if g < 2500:
        return "low"
    if g > 4000:
        return "macrosomia"
    return "normal"
