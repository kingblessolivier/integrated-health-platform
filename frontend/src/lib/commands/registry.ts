import type { ActionSpec } from "./types";

const SEX = ["female", "male"];

/**
 * Every command-bound endpoint the backend exposes today (mirrors each app's urls.py/views.py
 * and serializers, docs/49). Keyed by a unique id; `command` drives entitlement + audit.
 * The command bar shows only the actions whose command the caller holds; the server re-checks.
 */
export const ACTIONS: ActionSpec[] = [
  // ── Patients ────────────────────────────────────────────────────────────
  { id: "PTSR", command: "PTSR", domain: "Patients", label: "Search patients", method: "GET",
    path: "/patients/", fields: [{ name: "q", label: "Name or national ID" }] },
  { id: "PTRG", command: "PTRG", domain: "Patients", label: "Register patient", method: "POST",
    path: "/patients/", fields: [
      { name: "nida_id", label: "National ID", required: true },
      { name: "given_name", label: "Given name" },
      { name: "family_name", label: "Family name" },
      { name: "sex", label: "Sex", type: "select", options: SEX },
      { name: "birth_date", label: "Birth date", type: "date" },
    ] },
  { id: "PTVW", command: "PTVW", domain: "Patients", label: "View patient record", method: "GET",
    path: "/patients/{pk}/", fields: [{ name: "pk", label: "Patient ID", required: true }] },
  { id: "FHIR", command: "PTVW", domain: "Patients", label: "Export FHIR bundle", method: "GET",
    path: "/fhir/patients/{patient_id}/",
    fields: [{ name: "patient_id", label: "Patient ID", required: true }] },

  // ── Clinical ────────────────────────────────────────────────────────────
  { id: "ENHX", command: "ENHX", domain: "Clinical", label: "List encounters", method: "GET",
    path: "/encounters/", fields: [] },
  { id: "ENNW", command: "ENNW", domain: "Clinical", label: "Open encounter", method: "POST",
    path: "/encounters/", fields: [
      { name: "patient_id", label: "Patient ID", required: true },
      { name: "facility_id", label: "Facility ID" },
    ] },
  { id: "ENDX", command: "ENDX", domain: "Clinical", label: "Record diagnosis (ICD)", method: "POST",
    path: "/encounters/{encounter_id}/diagnoses/", fields: [
      { name: "encounter_id", label: "Encounter ID", required: true },
      { name: "icd_code", label: "ICD-10 code", required: true, placeholder: "e.g. J18.9" },
      { name: "note", label: "Note", type: "textarea" },
    ] },
  { id: "ENCL", command: "ENCL", domain: "Clinical", label: "Close encounter", method: "POST",
    path: "/encounters/{encounter_id}/close/",
    fields: [{ name: "encounter_id", label: "Encounter ID", required: true }] },

  // ── Pharmacy ────────────────────────────────────────────────────────────
  { id: "RXNW", command: "RXNW", domain: "Pharmacy", label: "Prescribe", method: "POST",
    path: "/prescriptions/", fields: [{ name: "encounter_id", label: "Encounter ID", required: true }] },
  { id: "RXDP", command: "RXDP", domain: "Pharmacy", label: "Dispense (FEFO)", method: "POST",
    path: "/dispenses/", fields: [
      { name: "product_id", label: "Product ID", required: true },
      { name: "facility_id", label: "Facility ID", required: true },
      { name: "quantity", label: "Quantity", type: "number", required: true },
    ] },

  // ── Stock ───────────────────────────────────────────────────────────────
  { id: "STIN", command: "STIN", domain: "Stock", label: "Stock inquiry", method: "GET",
    path: "/stock/", fields: [{ name: "facility_id", label: "Facility ID" }] },
  { id: "STRC", command: "STRC", domain: "Stock", label: "Receive goods", method: "POST",
    path: "/stock/receive/", fields: [
      { name: "facility_id", label: "Facility ID" },
      { name: "product_id", label: "Product ID" },
      { name: "batch", label: "Batch" },
      { name: "expiry_date", label: "Expiry date", type: "date" },
      { name: "quantity", label: "Quantity", type: "number", required: true },
    ] },
  { id: "STEX", command: "STEX", domain: "Stock", label: "Expiry monitor (90/60/30)", method: "GET",
    path: "/stock/expiring/", fields: [{ name: "facility_id", label: "Facility ID" }] },

  // ── Diagnostics ─────────────────────────────────────────────────────────
  { id: "LBOR", command: "LBOR", domain: "Diagnostics", label: "Order lab test", method: "POST",
    path: "/lab/orders/", fields: [{ name: "encounter_id", label: "Encounter ID", required: true }] },
  { id: "LBRS", command: "LBRS", domain: "Diagnostics", label: "Enter lab result", method: "POST",
    path: "/lab/orders/{order_id}/result/", fields: [
      { name: "order_id", label: "Order ID", required: true },
      { name: "analyte", label: "Analyte" },
      { name: "value", label: "Value", required: true },
      { name: "unit", label: "Unit" },
      { name: "ref_low", label: "Reference low", type: "number" },
      { name: "ref_high", label: "Reference high", type: "number" },
    ] },
  { id: "LBSN", command: "LBSN", domain: "Diagnostics", label: "Sign off lab result", method: "POST",
    path: "/lab/results/{result_id}/sign/",
    fields: [{ name: "result_id", label: "Result ID", required: true }] },
  { id: "IMOR", command: "IMOR", domain: "Diagnostics", label: "Order imaging", method: "POST",
    path: "/imaging/orders/", fields: [{ name: "encounter_id", label: "Encounter ID", required: true }] },
  { id: "IMSN", command: "IMSN", domain: "Diagnostics", label: "Sign imaging report", method: "POST",
    path: "/imaging/orders/{order_id}/report/", fields: [
      { name: "order_id", label: "Order ID", required: true },
      { name: "dicom_ref", label: "DICOM reference" },
      { name: "report", label: "Report", type: "textarea" },
    ] },

  // ── Billing & Claims ────────────────────────────────────────────────────
  { id: "PHPS", command: "PHPS", domain: "Billing", label: "Checkout / point-of-sale", method: "POST",
    path: "/checkout/", fields: [
      { name: "total", label: "Total", type: "number", required: true },
      { name: "covered_rate", label: "Insurer covered rate (0–1)", type: "number" },
      { name: "facility_id", label: "Facility ID" },
      { name: "patient_id", label: "Patient ID" },
      { name: "insurer_id", label: "Insurer ID" },
      { name: "msisdn", label: "Mobile money number" },
    ] },
  { id: "CLSC", command: "CLSC", domain: "Claims", label: "Scrub claim", method: "POST",
    path: "/claims/{claim_id}/scrub/", fields: [
      { name: "claim_id", label: "Claim ID", required: true },
      { name: "has_diagnosis", label: "Has diagnosis", type: "select", options: ["true", "false"] },
      { name: "billed_matches", label: "Billed matches", type: "select", options: ["true", "false"] },
    ] },
  { id: "CLRV", command: "CLRV", domain: "Claims", label: "Review claim", method: "POST",
    path: "/claims/{claim_id}/review/", fields: [
      { name: "claim_id", label: "Claim ID", required: true },
      { name: "decision", label: "Decision", type: "select", options: ["approve", "reject"], required: true },
    ] },
  { id: "CLST", command: "CLST", domain: "Claims", label: "Settlement status", method: "GET",
    path: "/claims/{claim_id}/", fields: [{ name: "claim_id", label: "Claim ID", required: true }] },

  // ── CBHI ────────────────────────────────────────────────────────────────
  { id: "CBEN", command: "CBEN", domain: "CBHI", label: "Enrol member", method: "POST",
    path: "/cbhi/members/", fields: [
      { name: "patient_id", label: "Patient ID", required: true },
      { name: "scheme", label: "Scheme", type: "select", options: ["mutuelle", "rssb", "private"] },
    ] },
  { id: "CBPR", command: "CBPR", domain: "CBHI", label: "Record premium", method: "POST",
    path: "/cbhi/premiums/", fields: [
      { name: "member_id", label: "Member ID", required: true },
      { name: "amount", label: "Amount", type: "number", required: true },
      { name: "period", label: "Period", placeholder: "e.g. 2026-07" },
    ] },
  { id: "CBFB", command: "CBFB", domain: "CBHI", label: "Fund balance", method: "GET",
    path: "/cbhi/fund/", fields: [] },

  // ── Supply chain ────────────────────────────────────────────────────────
  { id: "SCRO", command: "SCRO", domain: "Supply", label: "Reorder recommendation", method: "POST",
    path: "/supply/reorder/", fields: [
      { name: "daily_velocity", label: "Daily velocity", type: "number", required: true },
      { name: "lead_time_days", label: "Lead time (days)", type: "number", required: true },
      { name: "safety_stock", label: "Safety stock", type: "number" },
      { name: "on_hand", label: "On hand", type: "number" },
    ] },
  { id: "SCPO", command: "SCPO", domain: "Supply", label: "Purchase order", method: "POST",
    path: "/supply/orders/", fields: [
      { name: "facility_id", label: "Facility ID" },
      { name: "supplier_id", label: "Supplier ID" },
      { name: "total", label: "Total", type: "number" },
    ] },
  { id: "SCRV", command: "SCRV", domain: "Supply", label: "Receive purchase order", method: "POST",
    path: "/supply/orders/{po_id}/receive/",
    fields: [{ name: "po_id", label: "Purchase order ID", required: true }] },

  // ── Community ───────────────────────────────────────────────────────────
  { id: "CHIC", command: "CHIC", domain: "Community", label: "CHW iCCM visit", method: "POST",
    path: "/chw-visits/", fields: [
      { name: "patient_id", label: "Patient ID", required: true },
      { name: "village_id", label: "Village ID" },
      { name: "kind", label: "Kind", placeholder: "e.g. iccm" },
      { name: "payload", label: "Assessment (JSON)", type: "json", placeholder: '{"fever": true}' },
    ] },
  { id: "RFNW", command: "RFNW", domain: "Community", label: "Create referral", method: "POST",
    path: "/referrals/", fields: [
      { name: "patient_id", label: "Patient ID", required: true },
      { name: "from_facility", label: "From facility" },
      { name: "to_facility", label: "To facility" },
      { name: "context", label: "Context (JSON)", type: "json" },
    ] },
  { id: "RFRC", command: "RFRC", domain: "Community", label: "Receive referral by code", method: "GET",
    path: "/referrals/{code}/", fields: [{ name: "code", label: "Tracking code", required: true }] },

  // ── Emergency ───────────────────────────────────────────────────────────
  { id: "EMIN", command: "EMIN", domain: "Emergency", label: "SOS intake", method: "POST",
    path: "/emergency/sos/", fields: [
      { name: "patient_id", label: "Patient ID" },
      { name: "source", label: "Source", type: "select", options: ["sos", "912", "transfer"] },
    ] },
  { id: "EMDS", command: "EMDS", domain: "Emergency", label: "Dispatch nearest unit", method: "POST",
    path: "/emergency/dispatches/{dispatch_id}/assign/", fields: [
      { name: "dispatch_id", label: "Dispatch ID", required: true },
      { name: "origin", label: "Origin (JSON)", type: "json", placeholder: '{"lat": -1.95, "lng": 30.06}' },
      { name: "candidates", label: "Candidate units (JSON)", type: "json",
        placeholder: '[{"id":"u1","lat":-1.9,"lng":30.1}]' },
    ] },
  { id: "EMHO", command: "EMHO", domain: "Emergency", label: "Handover to ED", method: "POST",
    path: "/emergency/dispatches/{dispatch_id}/handover/", fields: [
      { name: "dispatch_id", label: "Dispatch ID", required: true },
      { name: "facility_id", label: "Destination facility" },
    ] },

  // ── Maternity ───────────────────────────────────────────────────────────
  { id: "MTDL", command: "MTDL", domain: "Maternity", label: "Delivery record", method: "POST",
    path: "/maternity/deliveries/", fields: [
      { name: "encounter_id", label: "Encounter ID" },
      { name: "patient_id", label: "Patient ID", required: true },
      { name: "outcome", label: "Outcome", type: "select",
        options: ["live_birth", "stillbirth", "miscarriage"] },
    ] },
  { id: "MTBR", command: "MTBR", domain: "Maternity", label: "Birth registration", method: "POST",
    path: "/maternity/births/", fields: [
      { name: "delivery_id", label: "Delivery ID", required: true },
      { name: "sex", label: "Sex", type: "select", options: SEX },
      { name: "weight_grams", label: "Weight (grams)", type: "number" },
    ] },

  // ── Regulatory ──────────────────────────────────────────────────────────
  { id: "RGDR", command: "RGDR", domain: "Regulatory", label: "Register drug", method: "POST",
    path: "/regulatory/drugs/", fields: [
      { name: "product_id", label: "Product ID", required: true },
      { name: "importer", label: "Importer" },
      { name: "expires_on", label: "Expires on", type: "date" },
    ] },
  { id: "RGPV", command: "RGPV", domain: "Regulatory", label: "Report adverse event", method: "POST",
    path: "/regulatory/adverse-events/", fields: [
      { name: "product_id", label: "Product ID", required: true },
      { name: "description", label: "Description", type: "textarea" },
      { name: "severity", label: "Severity", type: "select",
        options: ["mild", "moderate", "severe"] },
    ] },
  { id: "RGRC", command: "RGRC", domain: "Regulatory", label: "Recall drug", method: "POST",
    path: "/regulatory/drugs/{registration_id}/recall/",
    fields: [{ name: "registration_id", label: "Registration ID", required: true }] },

  // ── PBF ─────────────────────────────────────────────────────────────────
  { id: "PBSC", command: "PBSC", domain: "PBF", label: "PBF scoring", method: "POST",
    path: "/pbf/score/", fields: [
      { name: "metrics", label: "Metrics (JSON, 0–1)", type: "json", required: true,
        placeholder: '{"anc4": 0.8, "facility_delivery": 0.9}' },
      { name: "weights", label: "Weights (JSON, optional)", type: "json" },
      { name: "max_amount", label: "Max amount", type: "number", required: true },
    ] },
  { id: "PBAP", command: "PBAP", domain: "PBF", label: "Approve PBF payment", method: "POST",
    path: "/pbf/approve/", fields: [{ name: "amount", label: "Amount", type: "number", required: true }] },

  // ── HR & payroll ────────────────────────────────────────────────────────
  { id: "HRLC", command: "HRLC", domain: "Workforce", label: "Licence tracking", method: "GET",
    path: "/hr/licences/", fields: [] },
  { id: "PYRN", command: "PYRN", domain: "Workforce", label: "Run payroll", method: "POST",
    path: "/hr/payroll/run/", fields: [{ name: "gross", label: "Gross salary", type: "number", required: true }] },

  // ── Surveillance ────────────────────────────────────────────────────────
  { id: "SVMP", command: "SVMP", domain: "Surveillance", label: "Disease cluster map", method: "GET",
    path: "/surveillance/clusters/", fields: [] },
  { id: "SVAL", command: "SVAL", domain: "Surveillance", label: "Outbreak alerts", method: "GET",
    path: "/surveillance/alerts/",
    fields: [{ name: "threshold", label: "Threshold", type: "number", placeholder: "10" }] },

  // ── Security (SOC) ──────────────────────────────────────────────────────
  { id: "SELK", command: "SELK", domain: "Security", label: "Lock session (blacklist JWT)", method: "POST",
    path: "/security/lock/", fields: [{ name: "jti", label: "Token id (jti)", required: true }] },
  { id: "SEMR", command: "SEMR", domain: "Security", label: "Reset a user's MFA", method: "POST",
    path: "/security/mfa/reset/", fields: [{ name: "nida_id", label: "User national ID", required: true }] },
];

export const actionById = (id: string) => ACTIONS.find((a) => a.id === id);
