from apps.accounts.permissions import HoldsCommand


class _Req:
    def __init__(self, commands):
        self.auth = {"commands": commands}


class _View:
    required_command = "PTRG"


class _PublicView:
    required_command = None


def test_holds_command_allows_when_held():
    assert HoldsCommand().has_permission(_Req(["PTRG", "PTSR"]), _View()) is True


def test_holds_command_denies_when_missing():
    assert HoldsCommand().has_permission(_Req(["PTSR"]), _View()) is False


def test_holds_command_denies_without_auth():
    req = _Req([])
    req.auth = None
    assert HoldsCommand().has_permission(req, _View()) is False


def test_public_endpoint_allows_without_command():
    assert HoldsCommand().has_permission(_Req([]), _PublicView()) is True
