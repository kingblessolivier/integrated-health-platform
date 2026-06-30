from datetime import date, timedelta

from apps.stock.services import expiry_bucket, is_low_stock

TODAY = date(2026, 6, 30)


def test_expiry_buckets():
    assert expiry_bucket(TODAY - timedelta(days=1), TODAY) == "expired"
    assert expiry_bucket(TODAY + timedelta(days=15), TODAY) == "30"
    assert expiry_bucket(TODAY + timedelta(days=45), TODAY) == "60"
    assert expiry_bucket(TODAY + timedelta(days=80), TODAY) == "90"
    assert expiry_bucket(TODAY + timedelta(days=200), TODAY) == "ok"


def test_expiry_bucket_boundaries():
    assert expiry_bucket(TODAY, TODAY) == "30"            # 0 days -> within 30
    assert expiry_bucket(TODAY + timedelta(days=30), TODAY) == "30"
    assert expiry_bucket(TODAY + timedelta(days=31), TODAY) == "60"


def test_low_stock():
    assert is_low_stock(5) is True
    assert is_low_stock(10) is False
    assert is_low_stock(3, threshold=2) is False
