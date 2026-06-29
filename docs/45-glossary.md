# 45 — Glossary & Acronyms

Terms and acronyms used throughout this documentation. Rwanda-specific systems and
roles are marked where helpful.

## National systems & institutions

| Term | Meaning |
|---|---|
| **NIDA** | National Identification Agency — source of verified citizen identity/demographics |
| **DHIS2** | District Health Information System 2 — national health reporting / HMIS platform |
| **eIDSR** | Electronic Integrated Disease Surveillance and Response — disease-surveillance engine |
| **RSSB** | Rwanda Social Security Board — insurance clearing house (mutuelle / RAMA / pension) |
| **KWIVUZA** | RSSB's insurance / claims platform |
| **RMS** | Rwanda Medical Supply — national procurement, central warehousing, distribution |
| **SAMU 912** | National emergency medical service / ambulance dispatch (912 hotline) |
| **E-Banguka** | Emergency-response service integrated for dispatch |
| **RRA** | Rwanda Revenue Authority |
| **RRA EBM (2.0)** | Electronic Billing Machine — RRA's certified tax-invoicing rails |
| **RBC** | Rwanda Biomedical Centre — national disease-programme management (HIV, TB, malaria, immunisation) |
| **Rwanda FDA** | Food and Drugs Authority — drug registration, licensing, pharmacovigilance, recalls |
| **MoH** | Ministry of Health |
| **UNHCR ProGres** | UNHCR refugee registration system (humanitarian identity) |
| **NIDA / civil registration** | Birth and death events feeding national vital statistics |

## Roles & actors

| Term | Meaning |
|---|---|
| **CHW** | Community Health Worker — *umujyanama w'ubuzima* |
| **binôme** | The male–female CHW pair operating at village level |
| **ASM** | *Agent de Santé Maternelle* — maternal & newborn community health worker |
| **DHO** | District Health Officer |
| **CBHI** | Community-Based Health Insurance (the mutuelle scheme) |
| **mutuelle** | Community health-insurance scheme |
| **RAMA** | Civil-servant / formal-sector health-insurance scheme |
| **SOC** | Security Operations Centre |
| **SRE / SysOps** | Site Reliability Engineering / systems operations |
| **ADT clerk** | Admission–Discharge–Transfer (reception) clerk |
| **OPD** | Outpatient Department |
| **ED** | Emergency Department |

## Clinical & operational

| Term | Meaning |
|---|---|
| **iCCM** | Integrated Community Case Management — guided decision trees for childhood illness |
| **RDT** | Rapid Diagnostic Test |
| **FEFO** | First-Expiring, First-Out — batch-selection rule at dispensing |
| **five rights** | Right patient, drug, dose, route, time — medication-administration check |
| **CPOE** | Computerised Provider Order Entry |
| **PACS** | Picture Archiving and Communication System (imaging) |
| **EMR / EHR** | Electronic Medical / Health Record |
| **HMIS** | Health Management Information System |
| **PBF** | Performance-Based Financing |
| **NCD** | Non-Communicable Disease |
| **DOT** | Directly Observed Treatment (TB) |
| **MPI** | Master Patient Index — duplicate detection/resolution |
| **trauma override** | Emergency access for an unidentified critical patient |

## Standards & technology

| Term | Meaning |
|---|---|
| **HL7 FHIR (R4)** | Fast Healthcare Interoperability Resources — health-data exchange standard |
| **DICOM** | Digital Imaging and Communications in Medicine |
| **ICD-10/11** | International Classification of Diseases — diagnosis coding |
| **ATC** | Anatomical Therapeutic Chemical — WHO drug-classification codes |
| **OIDC / OAuth 2.0** | Federated authentication / authorisation protocols |
| **JWT** | JSON Web Token — signed session token carrying access scope |
| **mTLS** | Mutual TLS — both parties authenticate each other |
| **RLS** | Row-Level Security (PostgreSQL) |
| **WAF** | Web Application Firewall |
| **HSM** | Hardware Security Module — key custody |
| **PostGIS** | Spatial extension for PostgreSQL |
| **WAL** | Write-Ahead Log (point-in-time recovery) |
| **RTO** | Recovery Time Objective |
| **MoMo** | Mobile Money (MTN MoMo / Airtel Money) |
| **USSD** | Unstructured Supplementary Service Data — feature-phone menu sessions |

## Platform concepts

| Term | Meaning |
|---|---|
| **command** | The atomic unit of access — a `<2-char domain><2-char action>` code (see [03](03-command-catalogue.md)) |
| **command bundle** | The set of commands assigned to a user |
| **four-axis model** | Access bounded by Role(command) · Geography · Tenant · Sensitivity |
| **altitude** | The sensitivity/identifiability level of data a role may see; rises → more aggregated |
| **tenant** | An organisation whose data is isolated from others (facility, insurer, NGO…) |
| **shared core** | One patient record · one medicine catalogue · one inventory ledger · one financial ledger |
| **audit chain** | Append-only, SHA-256-chained log of every sensitive action |
| **offline-first** | Edge nodes keep working without network; changes reconcile on reconnect |
| **`LOCK`** | Incident command that terminates a session, blacklists its JWT, and locks the account |
