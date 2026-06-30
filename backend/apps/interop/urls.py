from django.urls import path

from .views import PatientFhirExport

urlpatterns = [
    path("fhir/patients/<uuid:patient_id>/", PatientFhirExport.as_view(), name="fhir-patient"),
]
