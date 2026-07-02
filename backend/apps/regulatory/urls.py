from django.urls import path

from .views import AdverseEventReport, DrugRegister, Recall

urlpatterns = [
    path("regulatory/drugs/", DrugRegister.as_view(), name="drug-register"),               # RGDR
    path("regulatory/adverse-events/", AdverseEventReport.as_view(), name="adr"),           # RGPV
    path("regulatory/drugs/<uuid:registration_id>/recall/", Recall.as_view()),             # RGRC
]
