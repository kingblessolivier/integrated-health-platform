# 35. Multi-Tenancy and Data Isolation

## Purpose
Specify strict tenant isolation across database, cache, messaging, and runtime boundaries.

## Isolation Model
- Shared control plane, logically isolated data plane.
- Every request carries immutable `tenant_id` context.

## Database Isolation
- PostgreSQL Row-Level Security (RLS) enforced on tenant tables.
- Security-definer functions prohibited unless reviewed.
- Mandatory tenant predicate tests for all repository queries.

## Cache Isolation
- Redis key namespace: `{tenant_id}:{domain}:{key}`
- No shared key patterns without tenant prefix.
- Cache poisoning tests included in CI security suite.

## Message Isolation
- Queue topics partitioned by tenant where required.
- Consumer validates tenant context before processing.

## Kubernetes and Runtime Isolation
- Namespace segmentation for critical workloads.
- Network policies deny cross-tenant pod communication by default.
- RBAC grants scoped to service account and namespace.

## Test Controls
- Automated RLS bypass tests
- Cross-tenant access negative tests per release
- Cache isolation regression tests

## Incident Response
Any cross-tenant data access event:
1. Immediate containment and access suspension.
2. Forensic scope assessment.
3. Tenant notification and remediation plan.

