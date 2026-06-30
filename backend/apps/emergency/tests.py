from apps.emergency.services import Unit, haversine_km, nearest_unit


def test_haversine_one_degree_latitude_is_about_111km():
    d = haversine_km((30.0, 0.0), (30.0, 1.0))
    assert 110.0 < d < 112.0


def test_haversine_zero_distance():
    assert haversine_km((30.06, -1.94), (30.06, -1.94)) == 0.0


def test_nearest_unit_picks_closest():
    origin = (30.06, -1.94)  # Kigali-ish
    units = [
        Unit("far", 30.50, -2.40),
        Unit("near", 30.07, -1.95),
        Unit("mid", 30.20, -2.00),
    ]
    assert nearest_unit(origin, units).id == "near"


def test_nearest_unit_none_when_empty():
    assert nearest_unit((30.0, -1.9), []) is None
