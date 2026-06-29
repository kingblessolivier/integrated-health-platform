# 61 — Data Dictionary

Field-level definitions for the principal entities. Types are conceptual; physical types and
indexes are in [48 — Database Schema](48-database-schema.md). Conventions: [46](46-naming-conventions.md).

## patients
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | System patient identifier (opaque) |
| tenant_id | UUID | FK, not null | Owning organisation |
| nida_id | string(16) | unique if present | NIDA national ID (verified attribute) |
| is_temporary | boolean | default false | True for newborn/emergency/refugee identities |
| given_name | string | | First name |
| family_name | string | | Surname |
| sex | enum | male/female | Administrative sex |
| birth_date | date | | Date of birth |
| created_at | timestamptz | not null | Creation time |

## encounters
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Encounter identifier |
| tenant_id | UUID | not null | Tenant |
| facility_id | UUID | FK | Where the encounter occurred |
| patient_id | UUID | FK | Subject patient |
| status | enum | open/closed/referred | Lifecycle state (doc 59) |
| encounter_date | timestamptz | not null | Start time |
| created_by | UUID | FK staff | Author |

## prescriptions
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Prescription identifier |
| encounter_id | UUID | FK | Source encounter |
| code | string | unique | Short SMS/counter code |
| signed_by | UUID | FK staff | Prescribing clinician |
| signature | bytes | not null | Digital signature |
| created_at | timestamptz | not null | Sign time |

## products (medicine catalogue)
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Product identifier |
| name | string | not null | Display name |
| atc | string | | WHO ATC code |
| fda_reg | string | | Rwanda FDA registration |
| tax_category | enum | | EBM tax category |

## stock_items
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Stock line identifier |
| facility_id | UUID | FK | Holding facility |
| product_id | UUID | FK | Catalogue product |
| batch | string | not null | Batch/lot as printed |
| expiry_date | date | not null | Expiry (drives FEFO) |
| quantity | integer | ≥ 0 | Units on hand |
| shelf | string | | Shelf location |

## transactions
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Sale identifier |
| facility_id | UUID | FK | Selling facility |
| insurer_portion | money | | Amount billed to insurer |
| out_of_pocket | money | | Patient-paid amount |
| ebm_token | string | | RRA EBM certification token |
| transaction_date | timestamptz | not null | Sale time |

## claims
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | UUID | PK | Claim identifier |
| transaction_id | UUID | FK | Source transaction |
| insurer_id | UUID | FK tenant | Payer |
| status | enum | submitted/scrubbing/approved/disputed/paid/rejected | Lifecycle (doc 59) |
| reason_code | string | | Dispute/rejection reason |

## audit_log
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | bigint | PK, identity | Sequence |
| actor_id | UUID | not null | Who acted |
| command | char(4) | not null | Command executed |
| resource_type | string | not null | Affected entity type |
| resource_id | UUID | | Affected entity |
| payload_hash | string | not null | SHA-256 of payload |
| prev_hash | string | not null | Previous entry hash |
| current_hash | string | not null | Chain hash |
| ts | timestamptz | not null | Action time |

## Common enumerations
| Enum | Values |
|---|---|
| facility.level | chw, health_centre, district, provincial, referral |
| staff.max_sensitivity | individual, facility, aggregate |
| tenant.kind | facility, insurer, ngo, camp, supplier |
| encounter.status | open, closed, referred |
| claim.status | submitted, scrubbing, approved, disputed, paid, rejected |
| op_log.status | pending, syncing, synced, conflict |
