from django.urls import path

from .views import CheckoutCreate

urlpatterns = [
    path("checkout/", CheckoutCreate.as_view(), name="checkout"),  # PHPS + PHSP + PHMM + PHEB
]
