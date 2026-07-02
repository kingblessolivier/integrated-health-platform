"""
HR & payroll endpoints (docs/03, docs/18): HRLC licence tracking, PYRN payroll run
(PAYE + RSSB → net). Reuses the community Licence model. Command-bound + audited.
"""
from datetime import date

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Licence
from .services import compute_paye, compute_rssb, licence_status, net_pay


class LicenceTracking(APIView):
    required_command = "HRLC"

    def get(self, request):
        today = date.today()
        rows = [{"staff_id": str(lic.staff_id), "council": lic.council,
                 "expires_on": lic.expires_on, "status": licence_status(lic.expires_on, today)}
                for lic in Licence.objects.all()[:500]]
        return Response({"licences": rows})


class PayrollRun(APIView):
    required_command = "PYRN"

    def post(self, request):
        c = request.auth or {}
        try:
            gross = float(request.data.get("gross", 0))
        except (TypeError, ValueError):
            return Response({"error": {"code": "INVALID_AMOUNT", "command": "PYRN"}}, status=422)
        if gross <= 0:
            return Response({"error": {"code": "INVALID_AMOUNT", "command": "PYRN"}}, status=422)
        paye, rssb = compute_paye(gross), compute_rssb(gross)
        result = {"gross": gross, "paye": paye, "rssb": rssb, "net": net_pay(gross)}
        audit.append(c.get("user_id"), "PYRN", "payroll", None, result, c.get("tenant_id"))
        return Response(result)
