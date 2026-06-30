"""
Claims pipeline endpoints (docs/03, docs/12): CLSC run scrubbing, CLRV review a disputed
claim, CLST settlement status. Reuses the Claim model from the billing app. All audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit
from apps.billing.models import Claim

from .services import advance, scrub


class ScrubClaim(APIView):
    required_command = "CLSC"

    def post(self, request, claim_id):
        c = request.auth or {}
        claim = Claim.objects.filter(id=claim_id).first()
        if claim is None:
            return Response(status=404)
        passed, reason = scrub(
            claim.amount,
            has_diagnosis=bool(request.data.get("has_diagnosis", True)),
            billed_matches=bool(request.data.get("billed_matches", True)),
        )
        claim.status = advance("submitted", "scrub_start")  # -> scrubbing
        claim.status = advance(claim.status, "scrub_pass" if passed else "scrub_flag")
        claim.reason_code = reason
        claim.save(update_fields=["status", "reason_code"])
        audit.append(c.get("user_id"), "CLSC", "claim", claim.id,
                     {"passed": passed, "reason": reason}, c.get("tenant_id"))
        return Response({"claim_id": str(claim.id), "status": claim.status, "reason_code": reason})


class ReviewClaim(APIView):
    required_command = "CLRV"

    def post(self, request, claim_id):
        c = request.auth or {}
        decision = request.data.get("decision")
        event = {"approve": "review_accept", "reject": "review_reject"}.get(decision)
        if event is None:
            return Response({"error": {"code": "BAD_DECISION", "command": "CLRV"}}, status=422)
        claim = Claim.objects.filter(id=claim_id).first()
        if claim is None:
            return Response(status=404)
        try:
            claim.status = advance(claim.status, event)
        except ValueError:
            return Response({"error": {"code": "INVALID_STATE", "command": "CLRV",
                                       "message": f"cannot review a claim in '{claim.status}'"}},
                            status=422)
        claim.save(update_fields=["status"])
        audit.append(c.get("user_id"), "CLRV", "claim", claim.id,
                     {"decision": decision}, c.get("tenant_id"))
        return Response({"claim_id": str(claim.id), "status": claim.status})


class SettlementStatus(APIView):
    required_command = "CLST"

    def get(self, request, claim_id):
        claim = Claim.objects.filter(id=claim_id).first()
        if claim is None:
            return Response(status=404)
        return Response({"claim_id": str(claim.id), "status": claim.status,
                         "reason_code": claim.reason_code, "amount": str(claim.amount)})
