from apps.audit.services import _sha256


def test_sha256_is_deterministic():
    assert _sha256("a", "b") == _sha256("a", "b")


def test_sha256_changes_with_input():
    assert _sha256("a") != _sha256("b")
