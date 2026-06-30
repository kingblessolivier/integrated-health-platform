from dataclasses import dataclass
from datetime import date, timedelta

from apps.pharmacy.services import select_fefo

TODAY = date(2026, 6, 29)


@dataclass
class Batch:
    expiry_date: date
    quantity: int
    batch: str = "X"


def d(days):
    return TODAY + timedelta(days=days)


def test_fefo_picks_earliest_in_date_batch():
    chosen = select_fefo(
        [Batch(d(30), 10, "A"), Batch(d(5), 10, "B"), Batch(d(60), 10, "C")], today=TODAY
    )
    assert chosen.batch == "B"


def test_fefo_skips_expired():
    chosen = select_fefo([Batch(d(-1), 10, "OLD"), Batch(d(10), 10, "NEW")], today=TODAY)
    assert chosen.batch == "NEW"


def test_fefo_skips_zero_quantity():
    chosen = select_fefo([Batch(d(1), 0, "EMPTY"), Batch(d(20), 5, "GOOD")], today=TODAY)
    assert chosen.batch == "GOOD"


def test_fefo_includes_batch_expiring_today():
    chosen = select_fefo([Batch(TODAY, 3, "TODAY")], today=TODAY)
    assert chosen.batch == "TODAY"


def test_fefo_returns_none_when_nothing_eligible():
    assert select_fefo([Batch(d(-1), 10, "OLD")], today=TODAY) is None
    assert select_fefo([], today=TODAY) is None
