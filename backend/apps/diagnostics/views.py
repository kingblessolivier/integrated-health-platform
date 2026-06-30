"""
Lab & imaging endpoints (docs/03): LBOR order, LBRS result entry (flags out-of-range via the
reference-interval classifier), LBSN sign-off; IMOR imaging order, IMSN signed report.
Command-bound, RLS-scoped, audited.
"""
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import ImagingReport, LabResult, Order
from .services import classify_result


class LabOrderCreate(APIView):
    required_command = "LBOR"

    def post(self, request):
        c = request.auth or {}
        order = Order.objects.create(tenant_id=c.get("tenant_id"),
                                     encounter_id=request.data.get("encounter_id"),
                                     type="lab", status="placed", created_by=c.get("user_id"))
        audit.append(c.get("user_id"), "LBOR", "order", order.id, {}, c.get("tenant_id"))
        return Response({"order_id": str(order.id), "status": "placed"}, status=201)


class LabResultEntry(APIView):
    required_command = "LBRS"

    def post(self, request, order_id):
        c = request.auth or {}
        flag = classify_result(request.data.get("value"), request.data.get("ref_low"),
                               request.data.get("ref_high"))
        result = LabResult.objects.create(
            tenant_id=c.get("tenant_id"), order_id=order_id,
            analyte=request.data.get("analyte", ""), value=str(request.data.get("value")),
            unit=request.data.get("unit"))
        Order.objects.filter(id=order_id).update(status="resulted")
        audit.append(c.get("user_id"), "LBRS", "lab_result", result.id,
                     {"flag": flag}, c.get("tenant_id"))
        return Response({"result_id": str(result.id), "flag": flag}, status=201)


class LabResultSignoff(APIView):
    required_command = "LBSN"

    def post(self, request, result_id):
        c = request.auth or {}
        updated = LabResult.objects.filter(id=result_id).update(
            signed_by=c.get("user_id"), signed_at=timezone.now())
        if not updated:
            return Response(status=404)
        audit.append(c.get("user_id"), "LBSN", "lab_result", result_id, {}, c.get("tenant_id"))
        return Response({"result_id": str(result_id), "status": "signed"})


class ImagingOrderCreate(APIView):
    required_command = "IMOR"

    def post(self, request):
        c = request.auth or {}
        order = Order.objects.create(tenant_id=c.get("tenant_id"),
                                     encounter_id=request.data.get("encounter_id"),
                                     type="imaging", status="placed", created_by=c.get("user_id"))
        audit.append(c.get("user_id"), "IMOR", "order", order.id, {}, c.get("tenant_id"))
        return Response({"order_id": str(order.id), "status": "placed"}, status=201)


class ImagingReportSign(APIView):
    required_command = "IMSN"

    def post(self, request, order_id):
        c = request.auth or {}
        report = ImagingReport.objects.create(
            tenant_id=c.get("tenant_id"), order_id=order_id,
            dicom_ref=request.data.get("dicom_ref"), report=request.data.get("report", ""),
            signature=b"", signed_by=c.get("user_id"), signed_at=timezone.now())
        Order.objects.filter(id=order_id).update(status="signed")
        audit.append(c.get("user_id"), "IMSN", "imaging_report", report.id, {},
                     c.get("tenant_id"))
        return Response({"report_id": str(report.id), "status": "signed"}, status=201)
