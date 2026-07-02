from apps.supply.services import reorder_quantity


def test_reorder_covers_lead_time_plus_safety_minus_on_hand():
    # 5/day * 14 days + 20 safety - 30 on hand = 60
    assert reorder_quantity(5, 14, 20, 30) == 60


def test_reorder_never_negative_when_overstocked():
    assert reorder_quantity(1, 7, 5, 1000) == 0


def test_reorder_rounds_up():
    assert reorder_quantity(2.5, 3, 0, 0) == 8  # 7.5 -> 8
