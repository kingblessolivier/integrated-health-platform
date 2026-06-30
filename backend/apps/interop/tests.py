from apps.interop.services import (
    build_patient_bundle,
    to_fhir_condition,
    to_fhir_encounter,
    to_fhir_patient,
)


def test_patient_maps_identifier_and_gender():
    r = to_fhir_patient({"id": "p1", "nida_id": "119", "given_name": "Aline",
                         "family_name": "U", "sex": "female"})
    assert r["resourceType"] == "Patient"
    assert r["identifier"][0]["value"] == "119"
    assert r["gender"] == "female"
    assert r["name"][0]["family"] == "U"


def test_patient_omits_empty_fields():
    r = to_fhir_patient({"id": "p1"})
    assert "identifier" not in r and "name" not in r and "gender" not in r


def test_encounter_status_mapping():
    assert to_fhir_encounter({"id": "e1", "patient_id": "p1", "status": "open"})["status"] == "in-progress"
    assert to_fhir_encounter({"id": "e1", "patient_id": "p1", "status": "closed"})["status"] == "finished"


def test_condition_uses_icd10_system():
    r = to_fhir_condition({"id": "d1", "encounter_id": "e1", "icd_code": "B54"})
    assert r["code"]["coding"][0]["system"] == "http://hl7.org/fhir/sid/icd-10"
    assert r["code"]["coding"][0]["code"] == "B54"


def test_bundle_structure_and_counts():
    bundle = build_patient_bundle(
        {"id": "p1", "given_name": "A"},
        encounters=[{"id": "e1", "patient_id": "p1", "status": "open"}],
        conditions=[{"id": "d1", "encounter_id": "e1", "icd_code": "B54"}],
    )
    assert bundle["resourceType"] == "Bundle"
    assert len(bundle["entry"]) == 3  # patient + 1 encounter + 1 condition
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert types == ["Patient", "Encounter", "Condition"]
