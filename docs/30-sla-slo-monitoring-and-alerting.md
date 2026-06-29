# 30. SLA, SLO, Monitoring, and Alerting Runbooks

## Purpose
Define measurable reliability objectives, alert thresholds, and actionable runbooks.

## SLA (External Commitment)
- Platform availability: **99.9% monthly**
- Incident acknowledgment: **<= 15 minutes** (P1)
- Data restoration after declared disaster: **<= 30 minutes RTO**

## SLO (Internal)
- API availability: 99.95%
- Clinical command success rate: >= 99.5%
- P95 read latency: < 500ms
- P95 write latency: < 2s
- External sync freshness (DHIS2/RSSB): < 15 minutes lag

## Error Budgets
- Monthly downtime budget for 99.9%: **43m 49s**
- If 50% of error budget consumed before day 15, freeze non-critical releases.

## Core Alert Thresholds
### Infrastructure
- CPU > 85% for 10m (warning), > 92% for 5m (critical)
- Memory > 90% for 10m
- Disk usage > 80% warning, > 90% critical

### Database
- Replication lag > 2s warning, > 10s critical
- Slow query P95 > 200ms warning, > 500ms critical
- Connection pool saturation > 85% for 5m

### Application
- 5xx rate > 1% warning, > 3% critical (5m window)
- P95 latency > 2x baseline for 10m
- Queue backlog > 70% warning, > 85% critical

### Security
- > 5 failed admin logins/min from single source
- Token replay anomaly detected
- Audit chain verification failure (immediate P1)

## Alert Routing
- P1 -> On-call SRE + Security lead + Product incident commander
- P2 -> On-call SRE
- P3 -> Team channel + next business day review

## Runbook Template (All Alerts)
1. Validate alert signal and scope.
2. Identify impacted services/tenants.
3. Mitigate first (throttle, failover, rollback).
4. Confirm recovery metrics stabilized.
5. Publish incident summary and follow-up actions.

## Specific Runbook: High 5xx
1. Check deployment timeline for recent release.
2. Inspect top failing endpoints and correlation IDs.
3. If release-correlated, execute rollback.
4. If dependency-correlated, force degraded mode and open circuits.
5. Verify error rate < 0.5% for 15m before closing incident.

## Specific Runbook: DB Replication Lag
1. Verify replica health and network latency.
2. Shift read traffic away from lagging replica.
3. Check long-running write transactions and lock contention.
4. Scale replica or restart replication process if stuck.

## Dashboard Minimums
- Golden signals per service: latency, traffic, errors, saturation
- Dependency status board
- Queue depth and DLQ trends
- Clinical workflow success funnel

