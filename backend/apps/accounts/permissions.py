"""
Command-driven, four-axis authorisation (see docs/04 and docs/49).

Not every resource is command-gated — the app works normally for ordinary, authenticated
use. Three access tiers:

  1. Public (anonymous) — set ``permission_classes = [AllowAny]`` on the view. Used for login
     (`/auth/token`), token refresh, health checks and other unauthenticated endpoints.
  2. Authenticated, no command — the DEFAULT under `HoldsCommand`: a valid token is required
     but no specific command. Use for normal app resources (own profile, reference/lookup
     data, MFA enrolment, dashboards that carry no identifiable PHI).
  3. Command-gated — the view declares ``required_command`` (and, for identifiable data,
     ``min_sensitivity``). The caller must HOLD that command in their JWT bundle and pass the
     geography/tenant/sensitivity checks. Used for privileged/sensitive actions.

A failure returns 403; the service layer additionally terminates the session, blacklists the
token, and writes an audit entry. Tenant is enforced by RLS; geography at the query layer via
`apps.accounts.access.in_geo_scope`.
"""
from rest_framework.permissions import BasePermission

from .access import sensitivity_ok


class HoldsCommand(BasePermission):
    """Requires authentication by default; enforces the command + sensitivity axes only when
    the view opts in via ``required_command``. Truly public endpoints bypass this class with
    ``permission_classes = [AllowAny]``."""

    message = "Caller does not hold the required command or is out of scope."

    def has_permission(self, request, view):
        claims = getattr(request, "auth", None)
        if not claims:
            return False  # tier 2/3 both require a valid token; public views use AllowAny
        required = getattr(view, "required_command", None)
        if required is None:
            return True  # tier 2: normal authenticated resource — no command needed
        # tier 3: role (command) axis
        if required not in set(claims.get("commands", [])):
            return False
        # sensitivity axis: the view's minimum data-identifiability vs the caller's ceiling.
        min_sensitivity = getattr(view, "min_sensitivity", None)
        if min_sensitivity and not sensitivity_ok(
            min_sensitivity, claims.get("max_sensitivity", "aggregate")
        ):
            return False
        return True
