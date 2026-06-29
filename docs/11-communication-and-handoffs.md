# 11 — Communication & Handoffs

Communication is primarily **structured data handoff through the shared record**. When one
actor writes, the next authorised actor reads, and the system notifies them automatically.
Secondary channels are in-platform notifications, SMS, and push alerts.

## Communication paths

| Path | Mechanism |
|---|---|
| CHW → health centre | Referral tracking code sent by SMS to parent; electronic referral appears instantly on the triage screen |
| Clinician → pharmacy | Digital prescription signed in CPOE; pharmacy receives it immediately; patient gets SMS code |
| Clinician → laboratory | Electronic order placed; lab receives in queue; results flow back and notify the clinician |
| Clinician → radiology | Imaging order placed; radiologist sees it in the PACS queue; signed report returns to the ordering clinician |
| Ambulance → emergency bay | Pre-hospital vitals and findings stream live to the ED before the vehicle arrives |
| Pharmacy → insurer | Claim batches transmitted electronically after each transaction; settlement status returned |
| Facility → district / national | Aggregated indicators pushed automatically on schedule; no manual report |
| District → facility | Stock-transfer instruction executed in the system; both facilities update instantly |
| System → patient | Appointment reminders, prescription-ready alerts, lab-result notifications via push (app) and SMS (feature phone) |
| Patient app → SAMU | SOS sends GPS coordinates directly to the SAMU console; creates a dispatch ticket automatically |
| Insurer → facility | Eligibility status returned at registration; claim approval/rejection with reconciliation code |
| Platform → DHIS2 / eIDSR | FHIR bundles pushed automatically every hour; no manual data entry at any tier |

## Principles

- The **record is the message**: a write by one actor becomes a read for the next, with an
  automatic notification — there is no parallel messaging silo to keep in sync.
- **SMS and USSD** guarantee reach to feature phones across Rwanda.
- **Critical notifications always have an SMS fallback** if push delivery fails.

> Every handoff is also an audit-chain event — *who · what · when* is recorded on each step.
