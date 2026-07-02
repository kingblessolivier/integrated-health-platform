from apps.cbhi.services import fund_balance


def test_fund_balance_positive():
    assert fund_balance(1_000_000, 400_000) == 600_000.0


def test_fund_balance_negative_when_overspent():
    assert fund_balance(100_000, 250_000) == -150_000.0


def test_fund_balance_rounds():
    assert fund_balance("100.005", "0.00") == 100.0
