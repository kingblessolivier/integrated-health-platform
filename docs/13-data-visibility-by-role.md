# 13 — Data Visibility by Role

Data visibility is governed by the **four-axis access model** (see
[04 — Access-Control Model](04-access-control-model.md)). As **altitude rises, data is
progressively aggregated and de-identified** — leadership sees rates, never a patient's name.

## Visibility matrix

| Actor | May see | May **not** see |
|---|---|---|
| CHW (*binôme* / ASM) | Their village patients — names, symptoms, kit stock, referral status | Patients from another village; clinical notes they did not write |
| Cell coordinator | Aggregated village health-kit balances; CHW activity logs | Individual patient clinical records |
| Sector / health-centre director | Facility encounters; CHW referrals; cooperative PBF; sector ledger | District-wide data; other facilities' patient records |
| District epidemiologist | Disease counts and clusters by village/sector; stock levels across facilities | Patient names or individual clinical notes |
| District CBHI manager | Mutuelle enrolment, premiums, claims by provider, fund balance | Clinical content of claims; patient diagnoses |
| Provincial coordinator | District-level aggregates; provincial-hospital performance | Facility-level individual records |
| MoH / DG of Health | National aggregated indicators; infrastructure performance; data quality; compliance logs | Any individually identifiable patient record |
| Rwanda FDA | Drug registration; import licences; adverse-reaction signals; recall compliance | Patient clinical records; financial transactions |
| RSSB | Claims pipeline; settlement status; aggregate utilisation by provider and scheme | Individual diagnoses beyond what the claim requires |
| Clinician (OPD) | Their patient's complete longitudinal record; orders they placed; results returned | Records of patients not in their care |
| Ward nurse | Assigned patients in their ward; medication schedule; bedside vitals | Patients on other wards; financial data |
| Pharmacist | Prescription details; stock levels; batch and expiry; transaction history | Other prescriptions beyond what is being dispensed |
| Pharmacy owner | Sales totals; insurer receivables; expiry exposure; margins — no patient names | Individual patient records; clinical details |
| Patient | Their own record only — appointments, prescriptions, results, bills, consent settings | Any other patient's data |
| Donor / multilateral | Anonymised, aggregated indicators for their funded programme only | Individual records; financial detail beyond programme-level spend |
| SOC / IT analyst | Security events, access logs, infrastructure metrics, audit-chain entries | Clinical content of patient records |

> **Data minimisation is enforced at query time:** a request returns only the fields the
> requesting role requires, never the whole record by default.
