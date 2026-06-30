from django.urls import path

from .views import (
    ImagingOrderCreate,
    ImagingReportSign,
    LabOrderCreate,
    LabResultEntry,
    LabResultSignoff,
)

urlpatterns = [
    path("lab/orders/", LabOrderCreate.as_view(), name="lab-order"),                       # LBOR
    path("lab/orders/<uuid:order_id>/result/", LabResultEntry.as_view()),                  # LBRS
    path("lab/results/<uuid:result_id>/sign/", LabResultSignoff.as_view()),                # LBSN
    path("imaging/orders/", ImagingOrderCreate.as_view(), name="imaging-order"),           # IMOR
    path("imaging/orders/<uuid:order_id>/report/", ImagingReportSign.as_view()),           # IMSN
]
