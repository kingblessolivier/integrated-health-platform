from decimal import Decimal

import pytest

from apps.billing.services import issue_ebm_receipt, momo_request_to_pay, split_payment


def test_split_full_out_of_pocket_when_uninsured():
    insurer, oop = split_payment("1000", 0)
    assert insurer == Decimal("0.00")
    assert oop == Decimal("1000")


def test_split_full_insurer_when_fully_covered():
    insurer, oop = split_payment("1000", 1)
    assert insurer == Decimal("1000.00")
    assert oop == Decimal("0.00")


def test_split_partial_coverage():
    insurer, oop = split_payment("1000", 0.9)
    assert insurer == Decimal("900.00")
    assert oop == Decimal("100.00")


def test_split_parts_always_sum_to_total_with_rounding():
    total = Decimal("1000.01")
    insurer, oop = split_payment(total, 0.85)
    assert insurer + oop == total  # remainder assigned to the patient


def test_split_rejects_bad_rate():
    with pytest.raises(ValueError):
        split_payment("100", 1.5)
    with pytest.raises(ValueError):
        split_payment("-1", 0.5)


def test_ebm_and_momo_token_formats():
    assert issue_ebm_receipt().startswith("EBM-")
    assert momo_request_to_pay(Decimal("10")).startswith("MOMO-")
    assert issue_ebm_receipt() != issue_ebm_receipt()  # unique
