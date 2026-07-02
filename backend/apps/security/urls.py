from django.urls import path

from .views import Lock, MfaConfirm, MfaEnrol, MfaReset

urlpatterns = [
    path("security/lock/", Lock.as_view(), name="security-lock"),  # SELK
    path("auth/mfa/enrol/", MfaEnrol.as_view(), name="mfa-enrol"),
    path("auth/mfa/confirm/", MfaConfirm.as_view(), name="mfa-confirm"),
    path("security/mfa/reset/", MfaReset.as_view(), name="mfa-reset"),  # SEMR (admin)
]
