# 12 — Operations Verification

Every operation passes through a **verification chain** before it is committed:

- **Technical** — the system checks the request.
- **Clinical** — a qualified person confirms.
- **Supervisory** — a higher level audits the aggregate output.

## Verification matrix

| Operation | Type | Mechanism |
|---|---|---|
| Drug dispensing | System | Batch barcode scanned; expiry and stock confirmed; five-rights check passed |
| Drug dispensing | Clinical | Pharmacist reviews and confirms before dispensing |
| Prescription | Clinical | Doctor signs with digital credentials; ICD code validated against diagnosis |
| Lab result | Clinical | Technologist reviews against reference intervals and signs off |
| Radiology report | Clinical | Radiologist applies a cryptographic digital signature |
| Surgery | Clinical | WHO surgical safety checklist stepped through on screen; each item confirmed |
| Insurance claim | System / AI | AI scrubbing engine cross-references diagnosis, lab results, dispensed batch, billed amount |
| Insurance claim | Supervisory | Claims auditor reviews AI-flagged disputes before rejection or payment |
| CHW reporting | System | GPS polygon confirms the CHW is in their village; iCCM logic validates the diagnostic flow |
| CHW reporting | Supervisory | Cell coordinator audits the physical kit against digital records |
| PBF payments | Supervisory | Sector officer evaluates cooperative targets; system computes the reward; officer approves |
| Payroll | System + supervisory | Statutory deductions computed automatically; accountant approves disbursement |
| Staff onboarding | System | NIDA identity verified; professional-council licence checked in real time |
| Access requests | System | JWT scope checked on every request; out-of-scope requests refused and logged |
| Audit chain | Cryptographic | Every sensitive action hashed and chained; any tampering breaks the chain |

> The principle: **no single actor both initiates and finally approves** a sensitive
> operation — the system, a clinician, and a supervisor each play a distinct role.
