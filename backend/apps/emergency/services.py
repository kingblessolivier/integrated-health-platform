"""
Pure dispatch logic (no DB) — unit-tested in tests.py.

Production dispatch uses a PostGIS spatial query (ST_DistanceSphere over ambulance geohashes,
docs/19). This haversine ranker is the equivalent in-process logic — used for ranking a
candidate set and as a fallback when PostGIS is unavailable.
"""
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

_EARTH_KM = 6371.0


@dataclass
class Unit:
    id: str
    lng: float
    lat: float


def haversine_km(a, b) -> float:
    """Great-circle distance in km between two (lng, lat) points."""
    lng1, lat1 = a
    lng2, lat2 = b
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    h = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return 2 * _EARTH_KM * asin(sqrt(h))


def nearest_unit(origin, units):
    """Return the Unit closest to `origin` ((lng, lat)), or None if there are no units."""
    if not units:
        return None
    return min(units, key=lambda u: haversine_km(origin, (u.lng, u.lat)))
