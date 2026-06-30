"""
Pure community-health logic (no DB) — unit-tested in tests.py. These run identically on the
server (validation) and on-device in the offline CHW app (docs/51): the GPS village-polygon
check and dose calculation must work without connectivity.
"""
import secrets


def generate_tracking_code() -> str:
    """Six-digit referral tracking code sent to the caregiver by SMS (docs/10, RFNW)."""
    return f"{secrets.randbelow(10 ** 6):06d}"


def point_in_polygon(point, polygon) -> bool:
    """Ray-casting point-in-polygon test.

    `point` is (lng, lat); `polygon` is a list of (lng, lat) vertices. Returns True if the
    point is inside. Used to confirm a CHW is within their assigned village polygon.
    """
    x, y = point
    n = len(polygon)
    if n < 3:
        return False
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def paediatric_dose_mg(weight_kg, mg_per_kg) -> float:
    """Weight-based dose (mg), rounded to 0.1 mg. Used by the iCCM RDT/dosing flow (CHRD)."""
    if weight_kg <= 0 or mg_per_kg <= 0:
        raise ValueError("weight_kg and mg_per_kg must be positive")
    return round(weight_kg * mg_per_kg, 1)
