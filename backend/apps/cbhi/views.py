"""
CBHI/mutuelle endpoints (docs/03, docs/20): CBEN enrol, CBPR record premium, CBFB fund
balance (premiums in minus claims paid out). Command-bound, RLS-scoped, audited on writes.
"""
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit
from apps.billing.models import Claim

from .models import CbhiMember, CbhiPremium
from .services import fund_balance


class Enrol(APIView):
    required_command = "CBEN"

    def post(self, request):
        c = request.auth or {}
        member = CbhiMember.objects.create(
            tenant_id=c.get("tenant_id"), patient_id=request.data.get("patient_id"),
            scheme=request.data.get("scheme", "mutuelle"))
        audit.append(c.get("user_id"), "CBEN", "cbhi_member", member.id, {}, c.get("tenant_id"))
        return Response({"member_id": str(member.id), "status": "active"}, status=201)


class RecordPremium(APIView):
    required_command = "CBPR"

    def post(self, request):
        c = request.auth or {}
        premium = CbhiPremium.objects.create(
            tenant_id=c.get("tenant_id"), member_id=request.data.get("member_id"),
            amount=request.data.get("amount", 0), period=request.data.get("period"))
        audit.append(c.get("user_id"), "CBPR", "cbhi_premium", premium.id,
                     {"amount": str(premium.amount)}, c.get("tenant_id"))
        return Response({"premium_id": str(premium.id)}, status=201)


class FundBalance(APIView):
    required_command = "CBFB"

    def get(self, request):
        premiums = CbhiPremium.objects.aggregate(s=Sum("amount"))["s"] or 0
        paid = Claim.objects.filter(status="paid").aggregate(s=Sum("amount"))["s"] or 0
        return Response({"premiums": str(premiums), "claims_paid": str(paid),
                         "balance": fund_balance(premiums, paid)})
