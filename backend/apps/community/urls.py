from django.urls import path

from .views import ChwVisitCreate, ReferralByCode, ReferralCreate

urlpatterns = [
    path("chw-visits/", ChwVisitCreate.as_view(), name="chw-visits"),       # CHIC
    path("referrals/", ReferralCreate.as_view(), name="referrals"),         # RFNW
    path("referrals/<str:code>/", ReferralByCode.as_view(), name="referral-by-code"),  # RFRC
]
