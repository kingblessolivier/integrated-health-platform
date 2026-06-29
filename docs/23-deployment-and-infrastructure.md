# 23 — Deployment & Infrastructure

## Deployment philosophy

- **Infrastructure as code:** every server, network rule, and configuration is defined in
  code (Terraform + Ansible) and version-controlled.
- **Immutable infrastructure:** updates replace containers with new ones rather than
  modifying running servers — eliminating configuration drift.
- **Blue-green deployments:** a new version is deployed to a parallel environment, tested,
  and traffic is switched in seconds; the old environment is kept for instant rollback.
- **Feature flags** enable or disable individual features without a deployment.

## CI/CD pipeline

- Every code merge triggers: unit tests, integration tests, static analysis, dependency
  vulnerability scan, container image build.
- Images that pass all checks are pushed to the **private container registry**.
- Deployment to staging is automatic; deployment to production requires a **manual approval
  gate**.
- Rollback is a one-command operation that redeploys the previous verified image.

## Environment structure

| Environment | Purpose |
|---|---|
| Development | Individual developer environments using Docker Compose |
| Staging | A full production replica for integration and partner-integration testing |
| Production | The live national system, on dedicated infrastructure within Rwanda |
| Disaster recovery | A hot-standby in a geographically separate data centre, continuously replicated |

## Data residency & hosting

- All personally identifiable health data is hosted **exclusively within Rwanda**.
- Backups are encrypted and stored within Rwanda.
- No patient data is transmitted to third-party cloud infrastructure outside Rwanda without
  explicit legal authorisation.

## High availability & failover

- **Patroni** manages PostgreSQL HA: a primary and at minimum two hot standbys in
  synchronous replication.
- If the primary fails, Patroni promotes a standby and redirects connections within
  **10 seconds**, with zero committed-transaction loss.
- Kubernetes reschedules crashed pods automatically across healthy nodes.
- **Redis** runs in sentinel mode with automatic failover for cache and session store.
- All critical services have **at minimum two running replicas** at all times.

## Offline-first rural & field nodes

- CHW phones, ambulance tablets, and rural facility terminals keep working without the
  network.
- Offline changes are queued and reconciled to the central ledger using a **conflict-
  resolution algorithm** when connectivity returns.
- A **sync-status banner** is always visible on mobile edges: green (synced) or amber
  (offline-autonomous).
- Critical safety checks use **locally cached decision tables** so they work without internet.
