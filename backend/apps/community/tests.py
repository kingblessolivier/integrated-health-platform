import pytest

from apps.community.services import (
    generate_tracking_code,
    paediatric_dose_mg,
    point_in_polygon,
)

# A unit square (lng/lat) 0,0 -> 1,1
SQUARE = [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_point_inside_polygon():
    assert point_in_polygon((0.5, 0.5), SQUARE) is True


def test_point_outside_polygon():
    assert point_in_polygon((1.5, 0.5), SQUARE) is False
    assert point_in_polygon((-0.1, 0.5), SQUARE) is False


def test_degenerate_polygon_is_never_inside():
    assert point_in_polygon((0.5, 0.5), [(0, 0), (1, 1)]) is False


def test_tracking_code_is_six_digits():
    for _ in range(50):
        code = generate_tracking_code()
        assert len(code) == 6 and code.isdigit()


def test_dose_calculation():
    assert paediatric_dose_mg(10, 15) == 150.0
    assert paediatric_dose_mg(7.5, 20) == 150.0


def test_dose_rejects_non_positive():
    with pytest.raises(ValueError):
        paediatric_dose_mg(0, 15)
    with pytest.raises(ValueError):
        paediatric_dose_mg(10, 0)
