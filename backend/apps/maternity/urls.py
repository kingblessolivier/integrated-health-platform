from django.urls import path

from .views import BirthRegister, DeliveryRecord

urlpatterns = [
    path("maternity/deliveries/", DeliveryRecord.as_view(), name="delivery"),  # MTDL
    path("maternity/births/", BirthRegister.as_view(), name="birth"),          # MTBR
]
