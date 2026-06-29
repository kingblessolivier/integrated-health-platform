"""
Patient endpoints. Each view binds to a command (docs/03); the HoldsCommand permission
checks the caller's bundle, RLS enforces tenant isolation, and the audit service records
the action. NIDA lookup is stubbed for the MVP (docs/64).
"""
from rest_framework import generics

from apps.audit import services as audit
from .models import Patient
from .serializers import PatientSerializer


def nida_lookup(nida_id: str) -> dict:
    """MVP stub — swap for the real NIDA adapter behind a circuit breaker (docs/09)."""
    return {"given_name": "Stub", "family_name": "Patient", "sex": "female"}


class PatientListCreate(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()  # RLS limits rows to the caller's tenant

    @property
    def required_command(self):
        return "PTRG" if self.request.method == "POST" else "PTSR"

    def perform_create(self, serializer):
        data = dict(serializer.validated_data)
        if data.get("nida_id"):
            data.update(nida_lookup(data["nida_id"]))
        claims = self.request.auth or {}
        obj = serializer.save(tenant_id=claims.get("tenant_id"), **{
            k: v for k, v in data.items() if k in {"given_name", "family_name", "sex"}
        })
        audit.append(claims.get("user_id"), "PTRG", "patient", obj.id,
                     {"nida_id": data.get("nida_id")}, claims.get("tenant_id"))


class PatientDetail(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    required_command = "PTVW"
