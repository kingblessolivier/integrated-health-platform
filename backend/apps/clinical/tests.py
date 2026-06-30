from apps.clinical.services import is_valid_icd


def test_icd_accepts_well_formed_codes():
    assert is_valid_icd("B54")      # malaria
    assert is_valid_icd("J18.9")    # pneumonia, unspecified organism
    assert is_valid_icd("A15.0")    # TB of lung


def test_icd_rejects_malformed_codes():
    assert not is_valid_icd("malaria")
    assert not is_valid_icd("")
    assert not is_valid_icd("123")
    assert not is_valid_icd("J189")  # missing dot
