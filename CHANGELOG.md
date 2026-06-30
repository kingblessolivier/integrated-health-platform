# Changelog

All notable changes to this project's documentation are recorded here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added (Stock & inventory)
- `stock` app: `STIN` inquiry, `STRC` receive goods (batch/expiry + movement), `STEX` expiry
  monitoring (90/60/30 buckets). Pure, unit-tested `expiry_bucket` + `is_low_stock`; reuses
  the pharmacy stock models.

### Added (Diagnostics — lab & imaging)
- `diagnostics` app: lab flow (`LBOR` order → `LBRS` result with reference-interval flagging
  → `LBSN` sign-off) and imaging (`IMOR` order → `IMSN` signed report). Pure, unit-tested
  `classify_result` (low/normal/high/unknown). Command-bound + audited.

### Added (Phase 5 — Surveillance & analytics)
- `surveillance` app: pure, unit-tested `aggregate_counts` + `detect_outbreaks` (threshold
  flagging) and de-identified endpoints `SVMP` (cluster counts) and `SVAL` (outbreak alerts).

### Added (Phase 5 — Interoperability, FHIR)
- `interop` app: a pure, unit-tested HL7 **FHIR R4** mapping (`to_fhir_patient/encounter/
  condition`, `build_patient_bundle`) + a command-bound `GET /fhir/patients/<id>/` export
  (Patient + Encounters + Conditions bundle) + a DHIS2 push stub.

### Added (Auth bootstrap)
- `bootstrap_user` management command: creates a Django auth user linked to a `staff` row +
  full command bundle, so `FourAxisTokenSerializer` issues real four-axis JWTs — closing the
  HTTP/JWT gap from doc 65. Generates/prints a random password (no secrets in code).
- `docs/65` updated with the HTTP path (`migrate` → `seed_commands` → `bootstrap_user` →
  token → curl) and the verified-vs-not table now marks the API as bootstrappable.

### Added (Verification harness)
- `backend/e2e/run_slice.py`: a data-layer end-to-end harness that seeds a minimal dataset and
  walks register → encounter → diagnosis → prescription → FEFO dispense → POS checkout → claim
  scrub/approve against a **real Postgres**, asserting the key invariants — exercising the
  actual schema, models, and business-logic services (no HTTP/JWT).
- `.github/workflows/e2e.yml`: CI job (TimescaleDB service + schema apply + the harness),
  using Postgres `trust` auth so there's no password literal.
- `docs/65-running-and-verifying.md`: how to run unit tests + the live e2e, and an honest
  "what's verified vs not" table, including the **HTTP/JWT auth-bootstrap gap** that blocks a
  full curl-against-the-API run.

### Added (Phase 4 — Finance & Claims, backend)
- `claims` app: `CLSC` run AI-scrubbing, `CLRV` review a disputed claim, `CLST` settlement
  status — reusing the billing `Claim` model, all audited.
- Pure, unit-tested pipeline logic: `advance` (claim state machine: submitted → scrubbing →
  approved/disputed → paid/rejected, rejects invalid transitions) and `scrub` (amount/
  diagnosis/match checks + high-amount-to-review routing).
- App registered, URLs wired, `seed_commands` extended with CL* codes.

### Added (Phase 3 — Emergency, backend)
- `emergency` app: `EMIN` SOS/intake creates a dispatch, `EMDS` assigns the nearest available
  unit, `EMHO` handover marks arrival — all audited.
- Pure, unit-tested dispatch logic: `haversine_km` and `nearest_unit` (the in-process
  equivalent of the production PostGIS proximity query).
- App registered, URLs wired, `seed_commands` extended with EM* codes.

### Added (Phase 2 — CHW offline, Flutter client core)
- Dependency-free Dart core for the offline CHW app: `pointInPolygon` (GPS village check)
  and `paediatricDoseMg` — mirrors the server services so device and server agree offline.
- `InMemoryOpLogDao` (concrete op-log) and a `dart:io`-based `SyncApi.push` that POSTs ops
  with the `Idempotency-Key` header for safe replay.
- Dart unit tests for the polygon check, dosing, and the sync-engine state transitions
  (synced / conflict / pending / idempotent-no-double-push).
- **Not verified in this environment** (no Flutter/Dart toolchain) — runs under `flutter test`
  once a toolchain or CI runner is available.

### Added (Phase 2 — CHW offline, backend)
- `community` app: `CHIC` record CHW visit (**idempotent** via `Idempotency-Key` for safe
  offline-op-log replay), `RFNW` create referral with a 6-digit tracking code (SMS stub),
  `RFRC` receive referral by code — all audited.
- Pure, unit-tested services shared by server and the on-device offline app: `point_in_polygon`
  (GPS village-polygon check), `generate_tracking_code`, `paediatric_dose_mg`.
- App registered, URLs wired, `seed_commands` extended with CH*/RF* codes.

### Added (POS & Billing)
- `billing` app: `PHPS` checkout that splits a total into insurer/out-of-pocket (`PHSP`),
  takes the co-payment via a MoMo stub (`PHMM`), issues an EBM certified-receipt token
  (`PHEB`), and queues an insurance claim when there's an insurer portion — one atomic,
  audited operation.
- Pure, unit-tested services: `split_payment` (exact-sum rounding, full/partial/zero
  coverage, input validation), `issue_ebm_receipt`, `momo_request_to_pay`.
- Registered the app, wired `/api/v1/checkout/`, and extended `seed_commands` with the PH* codes.

### Added (Phase 1 — Clinical Slice)
- `clinical` app: command-bound encounter endpoints (`ENNW` open, `ENHX` list, `ENDX`
  diagnosis with ICD-10 validation, `ENCL` close), each audited; pure `is_valid_icd` service
  with unit tests.
- `pharmacy` app: `RXNW` prescribe (signed, SMS code) and `RXDP` dispense under **FEFO** with
  atomic stock decrement + stock movement + audit; pure `select_fefo` service with unit tests
  (earliest-expiry, skips expired/zero-qty, includes expiring-today, empty cases).
- `seed_commands` management command to populate the command catalogue (idempotent).
- Registered both apps and wired their URLs under `/api/v1/`.

### Fixed
- CI scaffolding (Phase 0): frontend build script (`tsc && vite build`) and
  `vitest --passWithNoTests`; backend `pytest.ini` + first unit tests (audit hash,
  `HoldsCommand` permission); mobile `analysis_options.yaml` + smoke widget test.
- Removed the hardcoded Postgres password from `docker-compose.yml` (now required from
  `.env` via interpolation); added root `.env.example` and a `.gitignore` rule so
  `.env.example` files are tracked.

### Added
- Auth spine: `FourAxisTokenSerializer` issues a JWT carrying user/tenant/geo/sensitivity +
  the command bundle (`backend/apps/accounts/tokens.py`), wired into the login URL.
- **Project scaffolding**: Django + DRF backend skeleton (`backend/` — four-axis
  `HoldsCommand` permission, RLS `TenantContextMiddleware`, SHA-256 audit-chain service,
  sample patients app, runnable `sql/0001_initial.sql`), React + TS web skeleton
  (`frontend/` — command bar, entitlements, API client, design tokens), Flutter offline-first
- **Project scaffolding**: Django + DRF backend skeleton (`backend/` — four-axis
  `HoldsCommand` permission, RLS `TenantContextMiddleware`, SHA-256 audit-chain service,
  sample patients app, runnable `sql/0001_initial.sql`), React + TS web skeleton
  (`frontend/` — command bar, entitlements, API client, design tokens), Flutter offline-first
  skeleton (`mobile/` — op-log + sync engine), GitHub Actions CI for each, and `docker-compose.yml`.
- MVP scope & delivery roadmap (`docs/64-mvp-scope-and-roadmap.md`) — the Clinical Slice MVP
  plus a phased build plan.
- Reference docs: glossary & acronyms (`docs/45-glossary.md`), naming conventions
  (`docs/46-naming-conventions.md`), validation rules (`docs/47-validation-rules.md`).
- Implementation-contract docs: database schema & ERD (`docs/48-database-schema.md`),
  API contract / OpenAPI (`docs/49-api-contract.md`), frontend architecture
  (`docs/50-frontend-architecture.md`), and mobile & offline architecture
  (`docs/51-mobile-offline-architecture.md`).
- Repository meta files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, and this `CHANGELOG.md`.
- System Analysis & Design document set (`docs/52`–`docs/62`): Software Requirements
  Specification, Use Case Model, Data Flow Diagrams, Conceptual Data Model, Domain Class
  Diagram, Sequence Diagrams, Activity Diagrams, State Transition Diagrams, Component &
  Deployment Diagrams, Data Dictionary, and Requirements Traceability Matrix (Mermaid
  diagrams throughout).

- Full use-case catalogue (`docs/63-use-case-catalogue.md`) — a role-by-role account of what
  every user can do, grounded in the command bundles, with explicit boundaries per role.

### Changed
- `docs/48-database-schema.md`: expanded from excerpts into the complete, migration-ready
  schema — all ~30 tables, enums, indexes, RLS policies, triggers, partitioning, TimescaleDB,
  and FHIR mapping; mirrored as the runnable `backend/sql/0001_initial.sql`.
- Root `README.md`: added repository-layout and getting-started sections for the codebase.
- Root `README.md`: completed the stale documentation index (it listed only docs 01–26) —
  now a grouped, full index of all 63 docs plus project-meta links, with the corrected
  command count (~115 commands, 29 domains).
- `docs/03-command-catalogue.md`: added the Appointments (`AP`) domain (`APBK/APVW/APRS/APRM`)
  and wired it into the reception, clinician, and patient bundles; updated the count.
- `docs/53-use-case-model.md` and `docs/62-requirements-traceability-matrix.md`: reconciled
  command codes with the authoritative catalogue (e.g. `CHVS`→`CHIC/CHRD`, `EMDP`→`EMDS`).
- `docs/05-design-system.md`: fixed the failing amber state contrast (dark ink on amber;
  added darker `#B26A00` amber for foreground use), replaced the data-visualization palette
  with the colourblind-safe Okabe–Ito set, and added tonal-ramp / semantic-role token guidance.
- `docs/00-index.md`: added the reference/implementation-contract section (45–51) and a
  project-meta section.

## [0.2.0] — 2026-06-29

### Added
- Full-coverage documentation set mirroring the complete system specification —
  17 new docs (`docs/10`–`docs/26`): user workflows, communication & handoffs, operations
  verification, data visibility by role, analytics & dashboards, patient management, stock &
  pharmacy, supply chain, workforce & HR, ambulance & emergency, leadership & governance,
  threat monitoring & incident response, IT department responsibilities, deployment &
  infrastructure, database design & indexing, load balancing & performance, and conclusion.

## [0.1.0] — 2026-06-29

### Added
- Initial Integrated National Health Platform documentation: `README.md`, `LICENSE`,
  `.gitignore`, `CONTRIBUTING.md`, and the first nine docs (`docs/01`–`docs/09`):
  architecture, users & access, command catalogue, access-control model, design system,
  unified dashboard, technology stack, security & cryptography, and interoperability.
