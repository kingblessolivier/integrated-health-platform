from apps.maternity.services import classify_birth_weight


def test_low_birth_weight():
    assert classify_birth_weight(2400) == "low"


def test_normal_birth_weight():
    assert classify_birth_weight(3200) == "normal"


def test_macrosomia():
    assert classify_birth_weight(4200) == "macrosomia"


def test_boundaries():
    assert classify_birth_weight(2500) == "normal"
    assert classify_birth_weight(4000) == "normal"


def test_unknown():
    assert classify_birth_weight(None) == "unknown"
    assert classify_birth_weight(0) == "unknown"
