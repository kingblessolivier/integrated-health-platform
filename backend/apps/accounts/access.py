"""
Pure four-axis access helpers (docs/04, docs/08) — no DB, unit-tested in tests.py.
Role axis = HoldsCommand; tenant axis = RLS. These add the sensitivity and geography axes.
"""

# Higher = more identifiable. A caller may see data at or below their max sensitivity.
SENSITIVITY_ORDER = {"aggregate": 0, "facility": 1, "individual": 2}


def sensitivity_ok(required: str, held: str) -> bool:
    """True if a caller whose max sensitivity is `held` may access `required`-level data."""
    return SENSITIVITY_ORDER.get(held, -1) >= SENSITIVITY_ORDER.get(required, 99)


def in_geo_scope(target: dict, scope: dict) -> bool:
    """True if a `target` location falls within the caller's geographic `scope`.

    `scope` / `target` are dicts like {"district": "Karongi", "sector": "..."}. An empty
    scope means national (sees everything). Otherwise every level the caller is scoped to
    must match on the target (a missing level on the target is treated as out of scope).
    """
    if not scope:
        return True
    for level, value in scope.items():
        if target.get(level) != value:
            return False
    return True
