# 31. Backup, Recovery, and Disaster Recovery

## Metadata
- **Owner:** Infrastructure Team
- **Backup Owner:** Database Reliability Engineer
- **Last Reviewed:** 2026-06-29
- **Review Cadence:** Quarterly
- **Version:** 1.1

## Navigation
- **Index:** [00-index.md](./00-index.md)
- **Previous:** [30-sla-slo-monitoring-and-alerting.md](./30-sla-slo-monitoring-and-alerting.md)
- **Next:** [32-secrets-and-key-management.md](./32-secrets-and-key-management.md)
- **Related:** [23-deployment-and-infrastructure.md](./23-deployment-and-infrastructure.md), [24-database-design-and-indexing.md](./24-database-design-and-indexing.md), [44-documentation-and-runbooks.md](./44-documentation-and-runbooks.md)

## Purpose
Define recoverability controls, concrete RPO/RTO commitments, and tested failover procedures.

## Objectives
- **RPO**: <= 15 minutes for transactional clinical data
- **RTO**: <= 30 minutes for core services

## Backup Policy
- WAL/transaction-log shipping: continuous
- Full backup: daily at 01:00 CAT
- Incremental backup: every hour
- Retention:
  - Hourly: 48h
  - Daily: 35 days
  - Monthly: 12 months

## Storage and Geography
- Primary backups stored in Rwanda data center A
- Secondary encrypted copy stored in Rwanda data center B
- No backup storage outside approved jurisdiction

## Restore Runbook (Database)
1. Declare incident and freeze writes.
2. Select recovery point timestamp.
3. Restore full snapshot to recovery cluster.
4. Apply WAL until target timestamp.
5. Run integrity checks and clinical data validation set.
6. Switch traffic through controlled cutover.
7. Resume writes and monitor for 60 minutes.

## Application Recovery
- Stateless services redeployed from signed container registry.
- Config restored from versioned secure store.
- Message queues recovered from mirrored persistent volumes.

## DR Failover Modes
- **Automatic failover**: for single-node failures within primary site.
- **Manual failover**: cross-site disaster declaration with incident commander approval.

## DR Drill Schedule
- Tabletop exercise: monthly
- Partial technical drill: quarterly
- Full cross-site failover simulation: biannually

## Validation and Evidence
Each drill must record:
- Start/end timestamps
- Achieved RPO and RTO
- Data consistency findings
- Corrective actions and owner

## Replication Monitoring
- Track replication lag continuously.
- Critical alert if lag > 10s for 5m.
- Block failover if consistency checks fail.
