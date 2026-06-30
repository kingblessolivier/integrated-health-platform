from django.urls import path

from .views import ReviewClaim, ScrubClaim, SettlementStatus

urlpatterns = [
    path("claims/<uuid:claim_id>/scrub/", ScrubClaim.as_view(), name="claim-scrub"),     # CLSC
    path("claims/<uuid:claim_id>/review/", ReviewClaim.as_view(), name="claim-review"),   # CLRV
    path("claims/<uuid:claim_id>/", SettlementStatus.as_view(), name="claim-status"),     # CLST
]
