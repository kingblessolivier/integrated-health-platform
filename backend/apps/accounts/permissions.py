"""
Command-driven, four-axis authorisation (see docs/04 and docs/49).

Each view declares the command it requires via `required_command`. The caller must HOLD
that command (in their JWT bundle) and pass the geography/tenant/sensitivity checks.
A failure returns 403; the service layer additionally terminates the session, blacklists
the token, and writes an audit entry.
"""
from rest_framework.permissions import BasePermission


class HoldsCommand(BasePermission):
    message = "Caller does not hold the required command or is out of scope."

    def has_permission(self, request, view):
        required = getattr(view, "required_command", None)
        if required is None:
            return True  # public endpoint (e.g. token)
        claims = getattr(request, "auth", None)
        if not claims:
            return False
        commands = set(claims.get("commands", []))
        if required not in commands:
            return False
        # Geography / tenant / sensitivity are enforced at the data layer via RLS +
        # the service layer; this is the role(command) axis.
        return True
