import pytest

from apps.claims.services import advance, scrub


def test_happy_path_transitions():
    s = advance("submitted", "scrub_start")
    assert s == "scrubbing"
    assert advance(s, "scrub_pass") == "approved"
    assert advance("approved", "settle") == "paid"


def test_dispute_path_transitions():
    assert advance("scrubbing", "scrub_flag") == "disputed"
    assert advance("disputed", "review_accept") == "approved"
    assert advance("disputed", "review_reject") == "rejected"


def test_invalid_transition_raises():
    with pytest.raises(ValueError):
        advance("paid", "settle")
    with pytest.raises(ValueError):
        advance("submitted", "settle")


def test_scrub_passes_clean_claim():
    assert scrub("5000", has_diagnosis=True, billed_matches=True) == (True, None)


def test_scrub_flags_problems():
    assert scrub("0", has_diagnosis=True, billed_matches=True) == (False, "INVALID_AMOUNT")
    assert scrub("100", has_diagnosis=False, billed_matches=True) == (False, "NO_DIAGNOSIS")
    assert scrub("100", has_diagnosis=True, billed_matches=False) == (False, "AMOUNT_MISMATCH")


def test_scrub_routes_high_amount_to_review():
    passed, reason = scrub("2000000", has_diagnosis=True, billed_matches=True)
    assert passed is False and reason == "HIGH_AMOUNT_REVIEW"
