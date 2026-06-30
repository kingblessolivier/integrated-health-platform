from apps.diagnostics.services import classify_result


def test_classify_within_range_is_normal():
    assert classify_result(5.0, 4.0, 6.0) == "normal"


def test_classify_below_and_above():
    assert classify_result(3.0, 4.0, 6.0) == "low"
    assert classify_result(7.0, 4.0, 6.0) == "high"


def test_classify_open_bounds():
    assert classify_result(100, ref_low=10) == "normal"
    assert classify_result(5, ref_low=10) == "low"
    assert classify_result(100, ref_high=50) == "high"


def test_classify_non_numeric_is_unknown():
    assert classify_result("positive", 1, 2) == "unknown"
    assert classify_result(None) == "unknown"
