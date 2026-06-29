# 46 — Naming Conventions

How things are named across the platform. Consistent naming is what makes the system
**learnable, auditable, and interoperable** — a name means the same thing everywhere.

## Commands

The command is the atomic unit of access (see [03 — Command Catalogue](03-command-catalogue.md)).

- Format: **`<2-char domain><2-char action>`**, uppercase — e.g. `PTRG` (Patient · Register),
  `RXDP` (Prescription · Dispense), `ANVW` (Analytics · View).
- The **domain** is a stable 2-letter namespace (`PT`, `RX`, `LB`, `EN`, `CN`, …).
- The **action** is a 2-letter verb mnemonic (`RG` register, `VW` view, `SR` search,
  `NW` new, `ED` edit, `DP` dispense, `SN` sign-off, …).
- One command = one action on one resource. Never overload a code.
- New commands extend an existing domain where one fits; a new domain is added only for a
  genuinely new resource area, and must be documented in doc 03.

## Identifiers

| Identifier | Convention |
|---|---|
| Patient ID | Globally unique, system-issued, opaque (not the NIDA number); links every encounter |
| NIDA number | Stored as a verified attribute, validated against NIDA — never reused as the primary key |
| Temporary identity | Prefixed and flagged (`TMP-…`) for newborns / emergencies / refugees; reconciled later |
| Tenant ID | One per organisation (facility, insurer, NGO, camp); on every data-bearing row |
| Facility ID | One per physical site; on every data-bearing row alongside `tenant_id` |
| Encounter ID | System-issued per visit; immutable once created |
| Prescription code | Short, human-keyable code for the pharmacy counter / SMS (the `code` column) |
| Referral / tracking code | Six-digit code sent to the patient/parent by SMS |
| Batch / lot | Captured exactly as printed on stock; never normalised away |

## Database (PostgreSQL)

- Tables: **plural `snake_case`** — `patients`, `encounters`, `stock_items`, `audit_log`.
- Columns: **`snake_case`** — `patient_id`, `expiry_date`, `created_at`, `hash_chain`.
- Foreign keys: `<referenced_table_singular>_id` — `patient_id`, `facility_id`.
- Tenancy columns: every data-bearing table carries `tenant_id` and `facility_id`.
- Temporal columns: `valid_from` / `valid_to`, `created_at` / `updated_at`.
- Indexes: `idx_<table>_<cols>`; partial indexes named for their condition.

## API & integration

- REST resources: **plural, kebab/lower** nouns — `/patients`, `/stock-items`,
  `/prescriptions/{code}`.
- Verbs live in the HTTP method, not the path; sensitive operations map to a command code
  for audit.
- FHIR: standard **R4 resource names** (`Patient`, `Encounter`, `MedicationRequest`,
  `Observation`); profiles namespaced per Rwanda implementation guide.
- Codes: **ICD-10/11** for diagnoses, **WHO ATC** for drugs, **GeoJSON** admin codes for
  geography — always the standard code, never a local free-text alias.

## Code, branches & commits

- Branches: `feature/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`.
- Commits: imperative mood, concise subject — e.g. *"Add patient-management doc"*.
- Docs: **`NN-kebab-title.md`** under `docs/`, two-digit numeric prefix, listed in the
  index ([docs/00-index.md](00-index.md) and root `README.md`).
- Environment variables: `UPPER_SNAKE_CASE`; secrets never committed (see `.gitignore`).

> **Rule of thumb:** a name should be predictable from the thing it names. If a reader has
> to look it up twice, the convention has failed.
