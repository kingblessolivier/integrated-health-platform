from apps.accounts.access import in_geo_scope, sensitivity_ok
from apps.accounts.permissions import HoldsCommand


def test_sensitivity_ok():
    assert sensitivity_ok("individual", "individual") is True
    assert sensitivity_ok("aggregate", "individual") is True   # ceiling above requirement
    assert sensitivity_ok("individual", "aggregate") is False  # aggregate user, individual data
    assert sensitivity_ok("individual", "facility") is False


def test_in_geo_scope():
    assert in_geo_scope({"district": "Karongi"}, {}) is True                    # national
    assert in_geo_scope({"district": "Karongi"}, {"district": "Karongi"}) is True
    assert in_geo_scope({"district": "Nyamasheke"}, {"district": "Karongi"}) is False
    assert in_geo_scope({}, {"district": "Karongi"}) is False                   # missing level


class _SensitiveView:
    required_command = "PTVW"
    min_sensitivity = "individual"


class _Req:
    def __init__(self, auth):
        self.auth = auth


def test_permission_denies_aggregate_user_on_individual_view():
    req = _Req({"commands": ["PTVW"], "max_sensitivity": "aggregate"})
    assert HoldsCommand().has_permission(req, _SensitiveView()) is False


def test_permission_allows_individual_user_on_individual_view():
    req = _Req({"commands": ["PTVW"], "max_sensitivity": "individual"})
    assert HoldsCommand().has_permission(req, _SensitiveView()) is True
