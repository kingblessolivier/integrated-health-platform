"""
DRF exception handler that records access denials (docs/08: out-of-scope → 403 + log).
Wired via REST_FRAMEWORK['EXCEPTION_HANDLER'].
"""
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.views import exception_handler as drf_exception_handler

from apps.audit import services as audit


def audited_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if isinstance(exc, (PermissionDenied, NotAuthenticated)):
        request = context.get("request")
        claims = getattr(request, "auth", None) or {}
        actor = claims.get("user_id")
        if actor:  # only authenticated denials can be attributed in the audit chain
            try:
                audit.append(actor, "DENY", "access", None,
                             {"path": getattr(request, "path", "")}, claims.get("tenant_id"))
            except Exception:  # never let audit failure mask the 403
                pass
    return response
