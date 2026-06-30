from django.urls import path

from .views import DiagnosisCreate, EncounterClose, EncounterListCreate

urlpatterns = [
    path("encounters/", EncounterListCreate.as_view(), name="encounters"),            # ENNW/ENHX
    path("encounters/<uuid:encounter_id>/diagnoses/", DiagnosisCreate.as_view()),     # ENDX
    path("encounters/<uuid:encounter_id>/close/", EncounterClose.as_view()),          # ENCL
]
