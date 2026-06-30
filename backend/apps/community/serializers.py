from rest_framework import serializers

from .models import ChwVisit, Referral


class ChwVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChwVisit
        fields = ["id", "patient_id", "village_id", "kind", "payload", "gps_ok"]
        read_only_fields = ["id", "gps_ok"]


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ["id", "patient_id", "from_facility", "to_facility",
                  "tracking_code", "status", "context"]
        read_only_fields = ["id", "tracking_code", "status"]
