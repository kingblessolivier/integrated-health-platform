from django.urls import path

from .views import PbfApprove, PbfScore

urlpatterns = [
    path("pbf/score/", PbfScore.as_view(), name="pbf-score"),       # PBSC
    path("pbf/approve/", PbfApprove.as_view(), name="pbf-approve"),  # PBAP
]
