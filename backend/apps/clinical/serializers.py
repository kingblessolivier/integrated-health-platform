from rest_framework import serializers

from .models import Diagnosis, Encounter


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = ["id", "facility_id", "patient_id", "status", "encounter_date"]
        read_only_fields = ["id", "status", "encounter_date"]


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ["id", "encounter_id", "icd_code", "note"]
        read_only_fields = ["id", "encounter_id"]
