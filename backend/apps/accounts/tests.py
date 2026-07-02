from apps.accounts.permissions import HoldsCommand


class _Req:
    def __init__(self, commands):
        self.auth = {"commands": commands}


class _View:
    required_command = "PTRG"


class _NoCommandView:
    """Tier 2: normal authenticated resource — no command declared."""
    required_command = None


def test_holds_command_allows_when_held():
    assert HoldsCommand().has_permission(_Req(["PTRG", "PTSR"]), _View()) is True


def test_holds_command_denies_when_missing():
    assert HoldsCommand().has_permission(_Req(["PTSR"]), _View()) is False


def test_holds_command_denies_without_auth():
    req = _Req([])
    req.auth = None
    assert HoldsCommand().has_permission(req, _View()) is False


def test_no_command_view_allows_any_authenticated_user():
    # Tier 2: the app works normally — an authenticated caller needs no command here.
    assert HoldsCommand().has_permission(_Req([]), _NoCommandView()) is True


def test_no_command_view_still_requires_authentication():
    # A no-command view is NOT anonymous: without a token it is refused (public uses AllowAny).
    req = _Req([])
    req.auth = None
    assert HoldsCommand().has_permission(req, _NoCommandView()) is False
