"""
Sets PostgreSQL session variables from the authenticated JWT so row-level security
(see docs/48 section 10) is enforced for every query in the request.
"""
from django.db import connection


class TenantContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        claims = getattr(request, "auth", None)  # validated JWT payload (or None)
        if claims:
            tenant_id = claims.get("tenant_id")
            user_id = claims.get("user_id")
            with connection.cursor() as cur:
                # set_config(name, value, is_local=true) → scoped to this transaction.
                cur.execute("SELECT set_config('app.tenant_id', %s, true)", [str(tenant_id)])
                cur.execute("SELECT set_config('app.user_id', %s, true)", [str(user_id)])
        return self.get_response(request)
