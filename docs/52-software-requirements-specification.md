# 52 — Software Requirements Specification (SRS)

*Conforms to the spirit of IEEE 830 / ISO-IEC-IEEE 29148.*

## 1. Introduction

### 1.1 Purpose
This SRS specifies the requirements for the **Integrated National Health Platform** — the
orchestrating layer connecting Rwanda's health actors and sovereign national systems on one
shared core. It is the analysis-phase reference for design, implementation, and testing.

### 1.2 Scope
The platform provides one patient record, one medicine catalogue, one inventory ledger, and
one financial ledger, exposed through three faces (clinical, pharmacy, patient) and an
oversight layer, with command-driven access bounded by the four-axis model. It **integrates**
(does not replace) NIDA, DHIS2, eIDSR, RSSB/KWIVUZA, RMS, SAMU 912, and RRA EBM.

### 1.3 Definitions
See [45 — Glossary & Acronyms](45-glossary.md).

### 1.4 References
[01 Architecture](01-architecture.md) · [03 Command Catalogue](03-command-catalogue.md) ·
[04 Access-Control Model](04-access-control-model.md) ·
[09 Interoperability](09-interoperability.md) · [53 Use Case Model](53-use-case-model.md).

## 2. Overall description

### 2.1 Product perspective
A new operational system (clinical, pharmacy, community-health, patient experience) that
becomes the connective tissue between existing national systems. Four layers: Foundation →
Shared Core → Three Faces → Oversight.

### 2.2 User classes
| Class | Examples |
|---|---|
| Community | CHW (*binôme*), ASM, cell coordinator |
| Facility clinical | reception, clinicians, nurses, lab, radiology, midwives |
| Pharmacy & supply | dispensing pharmacist, cashier, owner, procurement, wholesalers |
| Patients | smartphone, feature-phone, caregiver, diaspora |
| District/national | DHO, epidemiologist, CBHI, provincial coordinator, MoH, RBC, FDA, RSSB |
| Back-office | HR, payroll, claims, IT/SOC |
| External | private insurers, donors, NGOs, suppliers, researchers, humanitarian |

### 2.3 Operating environment
Web (React), mobile (Flutter, offline-first), SMS/USSD, ambulance tablet; PostgreSQL core
hosted within Rwanda; intermittent rural connectivity.

### 2.4 Constraints
- Data residency: PHI hosted **exclusively within Rwanda** (Law N° 058/2021).
- Must operate offline at rural/field edges.
- Open standards: HL7 FHIR R4, DICOM, ICD-10/11, ATC.

### 2.5 Assumptions & dependencies
Partnership-gated access to NIDA, RSSB/KWIVUZA, RRA EBM, UNHCR ProGres; mobile-money and
SMS/USSD provider APIs available.

## 3. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Register a patient with NIDA-verified demographics; create temporary identity when unregistered | Must |
| FR-02 | Maintain one longitudinal record per patient across facilities (master patient index, dedup) | Must |
| FR-03 | Capture encounters: history, vitals, ICD-coded diagnosis, clinical notes | Must |
| FR-04 | Place CPOE orders (lab, imaging, medication) | Must |
| FR-05 | Create digitally signed prescriptions; deliver SMS code to patient | Must |
| FR-06 | Verify and dispense under FEFO with barcode batch/expiry checks; split insurer/out-of-pocket | Must |
| FR-07 | Generate and transmit an RRA-EBM certified invoice per sale | Must |
| FR-08 | Manage inventory by batch/lot/expiry; low-stock and expiry alerts; stock-take | Must |
| FR-09 | B2B marketplace: catalogue, reorder, purchase order, goods receiving | Should |
| FR-10 | CHW offline iCCM: GPS polygon check, decision trees, RDT dosing, referral codes | Must |
| FR-11 | Emergency: 912/SOS intake, nearest-ambulance dispatch, pre-hospital telemetry, handover | Must |
| FR-12 | Insurance: eligibility check, claim batch submission, AI scrubbing, settlement | Must |
| FR-13 | HR: NIDA + licence onboarding, scoped access provisioning, payroll with PAYE/RSSB | Should |
| FR-14 | Consent management: grant/revoke per actor; enforced with authorisation | Must |
| FR-15 | Command-driven access: users hold command bundles; UI renders from commands | Must |
| FR-16 | Role/geography/tenant/sensitivity scoping on every request | Must |
| FR-17 | Dashboards/analytics at each actor's altitude; real-time where data permits | Must |
| FR-18 | Push FHIR bundles to DHIS2/eIDSR hourly; no manual report | Must |
| FR-19 | Immutable, SHA-256-chained audit log of every sensitive action | Must |
| FR-20 | Offline capture with queued sync and conflict resolution on reconnect | Must |
| FR-21 | Patient portal/USSD: appointments, prescriptions, results, bills, find-care, MoMo pay | Must |

## 4. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | Patient registration < 2 s (p95); Rx code lookup < 500 ms; dashboard < 1 s |
| NFR-02 | Performance | EBM transmission < 3 s; FHIR hourly push < 30 s |
| NFR-03 | Availability | Critical services ≥ 2 replicas; DB failover < 10 s; HA + DR hot standby |
| NFR-04 | Scalability | Auto-scale stateless tier within 60 s during settlement surges |
| NFR-05 | Security | TLS 1.3 in transit; AES-256 at rest; MFA for clinical/admin; least privilege |
| NFR-06 | Privacy | Data minimisation; anonymisation before leaving clinical scope; consent first-class |
| NFR-07 | Compliance | Law N° 058/2021; data residency in Rwanda; forensic-grade audit chain |
| NFR-08 | Usability | WCAG 2.2 AA; icon+text (low-literacy); KIN/FR/EN; sunlight-readable |
| NFR-09 | Reliability | Offline-first edges; circuit breaker so no integration failure blocks care |
| NFR-10 | Interoperability | HL7 FHIR R4, DICOM, ICD, ATC; independently testable integrations |
| NFR-11 | Maintainability | IaC, CI/CD, blue-green, feature flags |
| NFR-12 | Observability | Metrics, structured logs, distributed tracing, 24/7 SOC |

## 5. External interface requirements

- **User interfaces:** command bar + unified dashboard (web); offline-first mobile; SMS/USSD.
- **Hardware:** barcode scanners, portable vitals monitors, IoT cold-chain sensors, ambulance tablets.
- **Software interfaces:** NIDA, RSSB/KWIVUZA, RRA EBM, DHIS2/eIDSR, SAMU/E-Banguka, UNHCR
  ProGres, MoMo, Africa's Talking, maps (see [09](09-interoperability.md)).
