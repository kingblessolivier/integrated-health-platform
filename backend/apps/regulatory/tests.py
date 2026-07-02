from datetime import date, timedelta

from apps.regulatory.services import registration_status

TODAY = date(2026, 6, 30)


def test_registration_valid():
    assert registration_status(TODAY + timedelta(days=200), TODAY) == "valid"


def test_registration_expiring():
    assert registration_status(TODAY + timedelta(days=30), TODAY) == "expiring"


def test_registration_expired():
    assert registration_status(TODAY - timedelta(days=1), TODAY) == "expired"


def test_registration_none_is_valid():
    assert registration_status(None, TODAY) == "valid"
