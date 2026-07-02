"""
Command-driven, four-axis authorisation (see docs/04 and docs/49).

Each view declares the command it requires via `required_command`. The caller must HOLD
that command (in their JWT bundle) and pass the geography/tenant/sensitivity checks.
A failure returns 403; the service layer additionally terminates the session, blacklists
the token, and writes an audit entry.
"""
from rest_framework.permissions import BasePermission

from .access import sensitivity_ok


class HoldsCommand(BasePermission):
    """Enforces the role (command) and sensitivity axes. Tenant is enforced by RLS; a view
    exposing identifiable data declares `min_sensitivity` (e.g. "individual") and the caller's
    JWT `max_sensitivity` must permit it. Geography is enforced at the query layer via
    `apps.accounts.access.in_geo_scope`."""

    message = "Caller does not hold the required command or is out of scope."

    def has_permission(self, request, view):
        required = getattr(view, "required_command", None)
        if required is None:
            return True  # public endpoint (e.g. token)
        claims = getattr(request, "auth", None)
        if not claims:
            return False
        if required not in set(claims.get("commands", [])):
            return False
        # Sensitivity axis: the view's minimum data-identifiability vs the caller's ceiling.
        min_sensitivity = getattr(view, "min_sensitivity", None)
        if min_sensitivity and not sensitivity_ok(
            min_sensitivity, claims.get("max_sensitivity", "aggregate")
        ):
            return False
        return True
