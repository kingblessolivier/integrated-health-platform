"""
Surveillance endpoints (docs/03): SVMP real-time cluster counts, SVAL outbreak alerts vs a
threshold. De-identified aggregates only (RLS-scoped); reads, so not audited.
"""
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.models import Diagnosis

from .services import detect_outbreaks


def _counts_by_icd():
    rows = Diagnosis.objects.values("icd_code").annotate(n=Count("id"))
    return {r["icd_code"]: r["n"] for r in rows}


class ClusterMap(APIView):
    required_command = "SVMP"

    def get(self, request):
        return Response({"counts": _counts_by_icd()})


class OutbreakAlerts(APIView):
    required_command = "SVAL"

    def get(self, request):
        try:
            threshold = int(request.query_params.get("threshold", 10))
        except (TypeError, ValueError):
            threshold = 10
        alerts = detect_outbreaks(_counts_by_icd(), default_threshold=threshold)
        return Response({"threshold": threshold, "alerts": alerts})
