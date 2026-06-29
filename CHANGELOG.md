# Changelog

All notable changes to this project's documentation are recorded here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
