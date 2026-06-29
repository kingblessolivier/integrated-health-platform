from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "nida_id", "is_temporary", "given_name", "family_name", "sex", "birth_date"]
        read_only_fields = ["id"]
