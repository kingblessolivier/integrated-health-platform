<div align="center">

# 🏥 Integrated National Health Platform

### One unified national health rail for Rwanda — every actor, one shared core

</div>

---

## Overview

The Integrated National Health Platform is the **orchestrating layer** that connects
every actor in Rwanda's health system — from the village community health worker
(*umujyanama w'ubuzima*) to the Minister of Health — on a single shared core.

It does **not** replace Rwanda's sovereign national systems (DHIS2, eIDSR,
RSSB/KWIVUZA, NIDA, RMS, SAMU 912, RRA EBM). It connects them at the point of care
and feeds them automatically.

> **Design principle:** *Build what is missing, integrate what the state already runs.*

## The shift to command-driven access

Unlike a traditional system where each role gets a hand-built dashboard, this
platform is **command-driven** (in the spirit of core-banking systems such as
Finacle):

- The **command** is the atomic unit of access.
- A **user** is created and **assigned a set of commands** (a command bundle).
- The **single unified dashboard** renders itself from whatever commands the user holds.
- Data is then bounded by the **four-axis** model: Role(command) · Geography · Tenant · Sensitivity.

There is **one dashboard**, not 40. What you see is the set of commands you are
entitled to, at your data altitude.

## Documentation

The full, always-current index lives in **[docs/00-index.md](docs/00-index.md)**. The 64
numbered documents are grouped below.

**Core architecture (01–07)**
- [01 — Architecture](docs/01-architecture.md) · [02 — Users & Access](docs/02-users-and-access.md) ·
  [03 — Command Catalogue](docs/03-command-catalogue.md) (~115 commands, 29 domains) ·
  [04 — Access-Control Model](docs/04-access-control-model.md) ·
  [05 — Design System](docs/05-design-system.md) ·
  [06 — Unified Dashboard](docs/06-unified-dashboard.md) ·
  [07 — Technology Stack](docs/07-technology-stack.md)

**Security, interoperability & operations base (08–14)**
- [08 — Security & Cryptography](docs/08-security-and-cryptography.md) ·
  [09 — Interoperability](docs/09-interoperability.md) ·
  [10 — User Workflows](docs/10-user-workflows.md) ·
  [11 — Communication & Handoffs](docs/11-communication-and-handoffs.md) ·
  [12 — Operations Verification](docs/12-operations-verification.md) ·
  [13 — Data Visibility by Role](docs/13-data-visibility-by-role.md) ·
  [14 — Analytics & Dashboards](docs/14-analytics-and-dashboards.md)

**Domain modules (15–20)**
- [15 — Patient Management](docs/15-patient-management.md) ·
  [16 — Stock & Pharmacy Management](docs/16-stock-and-pharmacy-management.md) ·
  [17 — Supply Chain Management](docs/17-supply-chain-management.md) ·
  [18 — Workforce & HR Management](docs/18-workforce-and-hr-management.md) ·
  [19 — Ambulance & Emergency Management](docs/19-ambulance-and-emergency-management.md) ·
  [20 — Leadership & Governance](docs/20-leadership-and-governance.md)

**Platform operations & infrastructure (21–26)**
- [21 — Threat Monitoring & Incident Response](docs/21-threat-monitoring-and-incident-response.md) ·
  [22 — IT Department Responsibilities](docs/22-it-department-responsibilities.md) ·
  [23 — Deployment & Infrastructure](docs/23-deployment-and-infrastructure.md) ·
  [24 — Database Design & Indexing](docs/24-database-design-and-indexing.md) ·
  [25 — Load Balancing & Performance](docs/25-load-balancing-and-performance.md) ·
  [26 — Conclusion](docs/26-conclusion.md)

**Reliability, compliance & governance (27–44)**
- [27 — Error Handling & Resilience](docs/27-error-handling-and-resilience.md) ·
  [28 — Mobile Sync & Conflict Resolution](docs/28-mobile-sync-and-conflict-resolution.md) ·
  [29 — Testing Strategy & QA](docs/29-testing-strategy-and-qa.md) ·
  [30 — SLA/SLO, Monitoring & Alerting](docs/30-sla-slo-monitoring-and-alerting.md) ·
  [31 — Backup, Recovery & DR](docs/31-backup-recovery-and-disaster-recovery.md) ·
  [32 — Secrets & Key Management](docs/32-secrets-and-key-management.md) ·
  [33 — Data Residency & Compliance](docs/33-data-residency-and-compliance.md) ·
  [34 — Audit Chain Integrity](docs/34-audit-chain-integrity.md) ·
  [35 — Multi-Tenancy & Data Isolation](docs/35-multi-tenancy-and-data-isolation.md) ·
  [36 — Payment & Financial Controls](docs/36-payment-and-financial-controls.md) ·
  [37 — Observability, Correlation & Tracing](docs/37-observability-correlation-and-tracing.md) ·
  [38 — API Versioning & Deprecation](docs/38-api-versioning-and-deprecation.md) ·
  [39 — Mobile App Security](docs/39-mobile-app-security.md) ·
  [40 — Access Lifecycle & Audit](docs/40-access-lifecycle-and-audit.md) ·
  [41 — Facility Onboarding & Migration](docs/41-facility-onboarding-and-migration.md) ·
  [42 — Rate Limiting & Quotas](docs/42-rate-limiting-and-quotas.md) ·
  [43 — Change Management & Release](docs/43-change-management-and-release.md) ·
  [44 — Documentation & Runbooks](docs/44-documentation-and-runbooks.md)

**Reference & implementation contracts (45–51)**
- [45 — Glossary & Acronyms](docs/45-glossary.md) ·
  [46 — Naming Conventions](docs/46-naming-conventions.md) ·
  [47 — Validation Rules](docs/47-validation-rules.md) ·
  [48 — Database Schema & ERD](docs/48-database-schema.md) ·
  [49 — API Contract](docs/49-api-contract.md) ·
  [50 — Frontend Architecture](docs/50-frontend-architecture.md) ·
  [51 — Mobile & Offline Architecture](docs/51-mobile-offline-architecture.md)

**System analysis & design (52–63)**
- [52 — Software Requirements Specification](docs/52-software-requirements-specification.md) ·
  [53 — Use Case Model](docs/53-use-case-model.md) ·
  [54 — Data Flow Diagrams](docs/54-data-flow-diagrams.md) ·
  [55 — Conceptual Data Model](docs/55-conceptual-data-model.md) ·
  [56 — Domain Class Diagram](docs/56-domain-class-diagram.md) ·
  [57 — Sequence Diagrams](docs/57-sequence-diagrams.md) ·
  [58 — Activity Diagrams](docs/58-activity-diagrams.md) ·
  [59 — State Transition Diagrams](docs/59-state-transition-diagrams.md) ·
  [60 — Component & Deployment Diagrams](docs/60-component-and-deployment-diagrams.md) ·
  [61 — Data Dictionary](docs/61-data-dictionary.md) ·
  [62 — Requirements Traceability Matrix](docs/62-requirements-traceability-matrix.md) ·
  [63 — Use Case Catalogue](docs/63-use-case-catalogue.md)

**Delivery:** [64 — MVP Scope & Delivery Roadmap](docs/64-mvp-scope-and-roadmap.md) ·
[65 — Running & Verifying Locally](docs/65-running-and-verifying.md)

**Project meta:** [Contributing](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md) ·
[Security Policy](SECURITY.md) · [Changelog](CHANGELOG.md)

## Repository layout

| Path | What |
|---|---|
| [`docs/`](docs/00-index.md) | The full specification, analysis & design (64 docs) |
| [`backend/`](backend/README.md) | Django + DRF API skeleton — auth (four-axis), RLS, audit chain, sample app |
| [`frontend/`](frontend/README.md) | React + TypeScript web skeleton — command bar, entitlements, design tokens |
| [`mobile/`](mobile/README.md) | Flutter offline-first skeleton — op-log + sync engine |
| `backend/sql/0001_initial.sql` | Canonical, runnable database schema (mirrors [doc 48](docs/48-database-schema.md)) |
| `docker-compose.yml` | Local stack: Postgres (TimescaleDB+PostGIS), Redis, API |

## Getting started (local)

```bash
# 1. bring up the stack (applies the schema on first run)
docker compose up -d

# 2. backend
cd backend && cp .env.example .env && pip install -r requirements.txt && python manage.py runserver

# 3. frontend (separate shell)
cd frontend && npm install && npm run dev
```

See [docs/64 — MVP Scope & Delivery Roadmap](docs/64-mvp-scope-and-roadmap.md) for what to build first.

## Status

Documentation and design specification. Specific regulatory approvals, data-hosting
agreements, and integration partnership contracts must be confirmed with the relevant
Rwandan authorities (Ministry of Health, RBC, Rwanda FDA, RSSB, RRA) and qualified
legal advisers before implementation commences.
