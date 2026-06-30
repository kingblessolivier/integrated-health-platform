from apps.pbf.services import compute_pbf_score, payment_for_score


def test_score_unweighted_average():
    assert compute_pbf_score({"timeliness": 1.0, "accuracy": 0.5}) == 75.0


def test_score_weighted():
    score = compute_pbf_score({"timeliness": 1.0, "accuracy": 0.0},
                              weights={"timeliness": 3, "accuracy": 1})
    assert score == 75.0


def test_score_empty_is_zero():
    assert compute_pbf_score({}) == 0.0


def test_payment_proportional():
    assert payment_for_score(75.0, 100000) == 75000.0
    assert payment_for_score(0, 100000) == 0.0


def test_payment_clamps_score():
    assert payment_for_score(150, 100000) == 100000.0
    assert payment_for_score(-10, 100000) == 0.0
