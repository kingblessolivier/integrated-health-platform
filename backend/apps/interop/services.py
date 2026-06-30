"""
Pure HL7 FHIR R4 mapping (no DB) — unit-tested in tests.py. Builds the bundles the platform
pushes to DHIS2/eIDSR and shares with partners (docs/09). Inputs are plain dicts so the
mapping is fully testable; views assemble the dicts from ORM rows.
"""

# open/closed/referred -> FHIR Encounter.status
_ENC_STATUS = {"open": "in-progress", "in_progress": "in-progress",
               "ordered": "in-progress", "referred": "in-progress", "closed": "finished"}


def _drop_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in (None, [], {})}


def to_fhir_patient(p: dict) -> dict:
    identifiers = []
    if p.get("nida_id"):
        identifiers.append({"system": "https://nida.gov.rw", "value": p["nida_id"]})
    name = _drop_none({"family": p.get("family_name"),
                       "given": [p["given_name"]] if p.get("given_name") else None})
    birth = p.get("birth_date")
    return _drop_none({
        "resourceType": "Patient",
        "id": str(p["id"]),
        "identifier": identifiers,
        "name": [name] if name else None,
        "gender": p.get("sex"),
        "birthDate": birth.isoformat() if hasattr(birth, "isoformat") else birth,
    })


def to_fhir_encounter(e: dict) -> dict:
    return _drop_none({
        "resourceType": "Encounter",
        "id": str(e["id"]),
        "status": _ENC_STATUS.get(e.get("status"), "unknown"),
        "subject": {"reference": f"Patient/{e['patient_id']}"},
    })


def to_fhir_condition(d: dict) -> dict:
    return _drop_none({
        "resourceType": "Condition",
        "id": str(d["id"]),
        "code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10",
                             "code": d["icd_code"]}]},
        "encounter": {"reference": f"Encounter/{d['encounter_id']}"},
    })


def build_bundle(resources, bundle_type: str = "collection") -> dict:
    return {"resourceType": "Bundle", "type": bundle_type,
            "entry": [{"resource": r} for r in resources]}


def build_patient_bundle(patient: dict, encounters=(), conditions=()) -> dict:
    resources = [to_fhir_patient(patient)]
    resources += [to_fhir_encounter(e) for e in encounters]
    resources += [to_fhir_condition(c) for c in conditions]
    return build_bundle(resources)


def push_bundle_to_dhis2(_bundle: dict) -> dict:
    """Stub for the DHIS2/eIDSR FHIR push (docs/09). Returns the accepted-for-delivery ack."""
    return {"status": "queued", "accepted": True}
