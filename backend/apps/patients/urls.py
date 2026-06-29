from django.urls import path

from .views import PatientDetail, PatientListCreate

urlpatterns = [
    path("patients/", PatientListCreate.as_view(), name="patients"),       # PTRG / PTSR
    path("patients/<uuid:pk>/", PatientDetail.as_view(), name="patient"),  # PTVW
]
