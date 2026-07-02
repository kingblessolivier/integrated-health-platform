from django.urls import path

from .views import Lock

urlpatterns = [
    path("security/lock/", Lock.as_view(), name="security-lock"),  # SELK
]
