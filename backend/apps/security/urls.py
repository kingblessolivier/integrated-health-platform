from django.urls import path

from .views import Lock, MfaConfirm, MfaEnrol

urlpatterns = [
    path("security/lock/", Lock.as_view(), name="security-lock"),  # SELK
    path("auth/mfa/enrol/", MfaEnrol.as_view(), name="mfa-enrol"),
    path("auth/mfa/confirm/", MfaConfirm.as_view(), name="mfa-confirm"),
]
