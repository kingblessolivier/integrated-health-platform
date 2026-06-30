from rest_framework import serializers

from .models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["id", "encounter_id", "code", "status"]
        read_only_fields = ["id", "code", "status"]
