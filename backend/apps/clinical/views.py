"""
Clinical endpoints, each bound to a command (docs/03): ENNW open encounter, ENHX list,
ENDX record diagnosis (ICD-validated), ENCL close. RLS scopes rows to the caller's tenant;
the audit service records every write.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit import services as audit

from .models import Encounter
from .serializers import DiagnosisSerializer, EncounterSerializer
from .services import is_valid_icd


class EncounterListCreate(generics.ListCreateAPIView):
    serializer_class = EncounterSerializer
    queryset = Encounter.objects.all()
    min_sensitivity = "individual"

    @property
    def required_command(self):
        return "ENNW" if self.request.method == "POST" else "ENHX"

    def perform_create(self, serializer):
        c = self.request.auth or {}
        obj = serializer.save(tenant_id=c.get("tenant_id"), created_by=c.get("user_id"))
        audit.append(c.get("user_id"), "ENNW", "encounter", obj.id,
                     {"patient_id": str(obj.patient_id)}, c.get("tenant_id"))


class DiagnosisCreate(generics.CreateAPIView):
    serializer_class = DiagnosisSerializer
    required_command = "ENDX"
    min_sensitivity = "individual"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not is_valid_icd(serializer.validated_data["icd_code"]):
            return Response(
                {"error": {"code": "ICD_INVALID", "command": "ENDX",
                           "message": "Diagnosis must carry a valid ICD-10 code."}},
                status=422,
            )
        c = request.auth or {}
        obj = serializer.save(tenant_id=c.get("tenant_id"),
                              encounter_id=kwargs["encounter_id"],
                              created_by=c.get("user_id"))
        audit.append(c.get("user_id"), "ENDX", "diagnosis", obj.id,
                     {"icd": obj.icd_code}, c.get("tenant_id"))
        return Response(self.get_serializer(obj).data, status=201)


class EncounterClose(APIView):
    required_command = "ENCL"

    def post(self, request, encounter_id):
        updated = Encounter.objects.filter(id=encounter_id).update(status="closed")
        if not updated:
            return Response(status=404)
        c = request.auth or {}
        audit.append(c.get("user_id"), "ENCL", "encounter", encounter_id, {},
                     c.get("tenant_id"))
        return Response({"id": str(encounter_id), "status": "closed"})
