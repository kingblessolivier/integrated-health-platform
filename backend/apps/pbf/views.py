"""
PBF endpoints (docs/03, docs/20): PBSC compute a score from submitted indicators and the
proportional payment; PBAP approve/trigger payment. Command-bound + audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .services import compute_pbf_score, payment_for_score


class PbfScore(APIView):
    required_command = "PBSC"

    def post(self, request):
        c = request.auth or {}
        metrics = request.data.get("metrics") or {}
        weights = request.data.get("weights")
        try:
            max_amount = float(request.data.get("max_amount", 0))
            metrics = {k: float(v) for k, v in metrics.items()}
        except (TypeError, ValueError):
            return Response({"error": {"code": "INVALID_METRICS", "command": "PBSC"}}, status=422)
        score = compute_pbf_score(metrics, weights)
        payment = payment_for_score(score, max_amount)
        audit.append(c.get("user_id"), "PBSC", "pbf", None,
                     {"score": score, "payment": payment}, c.get("tenant_id"))
        return Response({"score": score, "payment": payment})


class PbfApprove(APIView):
    required_command = "PBAP"

    def post(self, request):
        c = request.auth or {}
        audit.append(c.get("user_id"), "PBAP", "pbf", None,
                     {"approved_amount": request.data.get("amount")}, c.get("tenant_id"))
        return Response({"status": "approved", "amount": request.data.get("amount")})
