# 47 — Validation Rules

How the platform validates every operation. Validation is **layered** — the same data is
checked at progressively deeper tiers, and a failure at any tier stops the operation and is
logged. This complements the human verification chain in
[12 — Operations Verification](12-operations-verification.md).

## Validation tiers

| Tier | Where | What it checks |
|---|---|---|
| **Edge / client** | Mobile app, web SPA, WAF | Format, required fields, obvious malformed input; WAF drops SQLi/XSS at the edge |
| **API** | Django REST / FastAPI serializers | Type, range, enum, referential existence, business rules, **JWT scope** |
| **Domain** | Service layer | Cross-entity rules (e.g. ICD vs. diagnosis, FEFO, five rights) |
| **Database** | PostgreSQL constraints + RLS | Referential integrity, uniqueness, tenancy isolation, ACID atomicity |

> Client-side validation is for UX only. **Every rule is re-checked server-side** — the
> client is never trusted.

## Identity & access

- **NIDA validation:** the national ID is verified against NIDA at registration/onboarding;
  demographics are auto-populated, never hand-typed over a verified record.
- **Master Patient Index:** duplicate detection runs on create; suspected duplicates are
  flagged for `PTMG` (merge) rather than silently inserted.
- **Professional licence:** checked in real time against the relevant council registry; an
  expired/absent licence blocks assignment to clinical duties.
- **JWT scope:** every request's token is validated for role, geography, tenant, and
  sensitivity. Out-of-scope → **403**, session terminated, token blacklisted, event logged.

## Clinical

- **Diagnosis:** must carry a valid **ICD-10/11** code; the code is validated *against the
  recorded diagnosis* before a prescription can be signed.
- **Prescription sign-off:** requires the clinician's digital credentials (digital signature).
- **Medication administration:** the **five rights** (patient, drug, dose, route, time) are
  enforced by scanning the wristband and drug barcode at the bedside.
- **Allergy / interaction:** orders are checked against the patient's recorded allergies and
  chronic conditions.
- **Lab results:** validated against reference intervals and signed off by a technologist.

## Pharmacy, stock & finance

- **Catalogue membership:** a scanned product not in the registered master catalogue is
  rejected at POS.
- **FEFO:** the system enforces First-Expiring-First-Out batch selection at dispensing;
  expired batches cannot be dispensed.
- **Expiry & stock thresholds:** alerts fire at 90/60/30 days and below the safety stock level.
- **Transaction atomicity:** a sale and its stock decrement succeed or fail together (ACID).
- **Insurer/out-of-pocket split:** computed and validated against eligibility before payment.
- **EBM invoice:** every completed sale produces an RRA-certified invoice; the certification
  token is validated on return.
- **Claims scrubbing:** the AI engine cross-references diagnosis, lab results, dispensed
  batch, and billed amount; mismatches are flagged for supervisory review before payment.

## Community & geospatial

- **GPS polygon check:** a CHW's record is validated to originate **inside their assigned
  village polygon** (works offline via cached boundaries).
- **iCCM logic:** the decision tree validates that the diagnostic flow is internally
  consistent before a case is accepted.
- **Dose calculation:** auto-computed from age and weight; the virtual kit is decremented
  only on a valid dispense.

## Data exchange & integrity

- **Schema validation:** outbound **FHIR R4** bundles and **EBM** payloads are validated
  against schema before transmission; invalid bundles are not pushed.
- **Webhook authenticity:** payment/EBM webhooks are validated with **HMAC-SHA256**
  signatures before they are acted on.
- **Audit chain:** each entry embeds the previous entry's **SHA-256** hash; chain integrity
  is verified on schedule, and any break is treated as a tampering incident.
- **Offline reconciliation:** queued offline changes pass a **conflict-resolution**
  algorithm on reconnect; conflicts are surfaced, not silently overwritten.

## Failure handling

- A failed validation **never** partially commits — the operation is rejected as a whole.
- Validation failures on sensitive operations are written to the audit chain.
- Where an external dependency is down (e.g. NIDA), the **circuit breaker** degrades
  gracefully (manual entry, deferred check) so care is never blocked — see
  [09 — Interoperability](09-interoperability.md).
