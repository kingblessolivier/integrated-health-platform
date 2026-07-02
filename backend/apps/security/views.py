"""
SOC endpoints (docs/03, docs/16): SELK LOCK — terminate a compromised session by
blacklisting its JWT id. Command-bound + audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .blacklist import blacklist_jti


class Lock(APIView):
    required_command = "SELK"

    def post(self, request):
        c = request.auth or {}
        jti = request.data.get("jti")
        if jti:
            blacklist_jti(jti)
        audit.append(c.get("user_id"), "SELK", "session", None, {"jti": jti},
                     c.get("tenant_id"))
        return Response({"status": "locked", "jti": jti})
