from django.urls import path

from .views import Enrol, FundBalance, RecordPremium

urlpatterns = [
    path("cbhi/members/", Enrol.as_view(), name="cbhi-enrol"),          # CBEN
    path("cbhi/premiums/", RecordPremium.as_view(), name="cbhi-premium"),  # CBPR
    path("cbhi/fund/", FundBalance.as_view(), name="cbhi-fund"),        # CBFB
]
