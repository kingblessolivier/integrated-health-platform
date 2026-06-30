from django.urls import path

from .views import DispenseCreate, PrescriptionCreate

urlpatterns = [
    path("prescriptions/", PrescriptionCreate.as_view(), name="prescriptions"),  # RXNW
    path("dispenses/", DispenseCreate.as_view(), name="dispenses"),              # RXDP
]
