from django.urls import path

from .views import LicenceTracking, PayrollRun

urlpatterns = [
    path("hr/licences/", LicenceTracking.as_view(), name="hr-licences"),  # HRLC
    path("hr/payroll/run/", PayrollRun.as_view(), name="hr-payroll"),     # PYRN
]
