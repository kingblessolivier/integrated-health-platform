"""
FHIR export endpoint (docs/09). Returns a patient's record as an HL7 FHIR R4 Bundle
(Patient + Encounters + Conditions). Bound to PTVW; RLS scopes rows; audited.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit
from apps.clinical.models import Diagnosis, Encounter
from apps.patients.models import Patient

from .services import build_patient_bundle


class PatientFhirExport(APIView):
    required_command = "PTVW"
    min_sensitivity = "individual"

    def get(self, request, patient_id):
        patient = Patient.objects.filter(id=patient_id).first()
        if patient is None:
            return Response(status=404)
        encounters = list(Encounter.objects.filter(patient_id=patient_id).values(
            "id", "patient_id", "status"))
        enc_ids = [e["id"] for e in encounters]
        conditions = list(Diagnosis.objects.filter(encounter_id__in=enc_ids).values(
            "id", "encounter_id", "icd_code")) if enc_ids else []
        bundle = build_patient_bundle(
            {"id": patient.id, "nida_id": patient.nida_id, "given_name": patient.given_name,
             "family_name": patient.family_name, "sex": patient.sex,
             "birth_date": patient.birth_date},
            encounters, conditions,
        )
        c = request.auth or {}
        audit.append(c.get("user_id"), "PTVW", "fhir_bundle", patient.id,
                     {"entries": len(bundle["entry"])}, c.get("tenant_id"))
        return Response(bundle)
