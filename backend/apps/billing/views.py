"""
POS checkout (docs/03: PHPS sale, PHSP insurer/patient split, PHMM mobile-money, PHEB EBM
receipt). One atomic operation: create the transaction with the split, take the co-payment
(MoMo stub), issue the EBM certified receipt (stub), and queue an insurance claim when there
is an insurer portion. Every step is audited.
"""
from decimal import Decimal

from django.db import transaction as dbtx
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Claim, Payment, Transaction
from .services import issue_ebm_receipt, momo_request_to_pay, split_payment


class CheckoutCreate(APIView):
    required_command = "PHPS"

    @dbtx.atomic
    def post(self, request):
        c = request.auth or {}
        data = request.data
        try:
            total = Decimal(str(data.get("total", "0")))
            covered_rate = float(data.get("covered_rate", 0))
        except (TypeError, ValueError):
            return Response(
                {"error": {"code": "INVALID_AMOUNT", "command": "PHPS"}}, status=422
            )
        if total <= 0:
            return Response(
                {"error": {"code": "INVALID_AMOUNT", "command": "PHPS",
                           "message": "total must be positive."}},
                status=422,
            )

        insurer_portion, out_of_pocket = split_payment(total, covered_rate)
        ebm_token = issue_ebm_receipt({"total": str(total)})

        txn = Transaction.objects.create(
            tenant_id=c.get("tenant_id"), facility_id=data.get("facility_id"),
            patient_id=data.get("patient_id"), insurer_portion=insurer_portion,
            out_of_pocket=out_of_pocket, ebm_token=ebm_token,
        )

        if out_of_pocket > 0:
            Payment.objects.create(
                tenant_id=c.get("tenant_id"), transaction_id=txn.id, method="momo",
                status="pending", amount=out_of_pocket,
                provider_ref=momo_request_to_pay(out_of_pocket, data.get("msisdn")),
            )

        claim_id = None
        if insurer_portion > 0 and data.get("insurer_id"):
            claim = Claim.objects.create(
                tenant_id=c.get("tenant_id"), transaction_id=txn.id,
                insurer_id=data.get("insurer_id"), status="submitted", amount=insurer_portion,
            )
            claim_id = str(claim.id)

        audit.append(c.get("user_id"), "PHPS", "transaction", txn.id,
                     {"total": str(total), "insurer": str(insurer_portion),
                      "oop": str(out_of_pocket)}, c.get("tenant_id"))

        return Response(
            {"transaction_id": str(txn.id), "ebm_token": ebm_token,
             "insurer_portion": str(insurer_portion), "out_of_pocket": str(out_of_pocket),
             "claim_id": claim_id},
            status=201,
        )
