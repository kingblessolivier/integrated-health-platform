from datetime import date, timedelta

from apps.hr.services import compute_paye, compute_rssb, licence_status, net_pay


def test_paye_zero_band():
    assert compute_paye(50000) == 0.0


def test_paye_progressive():
    assert compute_paye(80000) == 2000.0          # 20000 @ 10%
    assert compute_paye(150000) == 14000.0        # 4000 + 50000@20%
    assert compute_paye(250000) == 39000.0        # 4000 + 20000 + 15000


def test_rssb_three_percent():
    assert compute_rssb(100000) == 3000.0


def test_net_pay():
    # gross 150000: paye 14000, rssb 4500 -> net 131500
    assert net_pay(150000) == 131500.0


def test_licence_status():
    today = date(2026, 6, 30)
    assert licence_status(today - timedelta(days=1), today) == "expired"
    assert licence_status(today + timedelta(days=20), today) == "30"
    assert licence_status(today + timedelta(days=200), today) == "ok"
