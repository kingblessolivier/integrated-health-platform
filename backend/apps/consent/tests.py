from apps.consent.services import consent_permits


def test_allows_when_no_records():
    assert consent_permits([], "staff-1") is True


def test_allows_when_actor_granted():
    assert consent_permits([("staff-1", "granted")], "staff-1") is True


def test_denies_when_actor_revoked():
    assert consent_permits([("staff-1", "revoked")], "staff-1") is False


def test_other_actor_revocation_does_not_block():
    assert consent_permits([("staff-2", "revoked")], "staff-1") is True
