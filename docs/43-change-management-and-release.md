# 43. Change Management and Release Process

## Purpose
Define controlled release governance, approvals, and rollback criteria.

## Release Cadence
- Standard release window: weekly scheduled slot.
- Emergency hotfix path with expedited approvals.

## Change Classes
- Standard
- High-risk
- Emergency

## Required Approvals
- Engineering owner
- QA owner
- Clinical governance representative (for clinical-impacting changes)
- Security approval (for auth/crypto/identity changes)

## Release Stages
1. Plan and risk assessment
2. Staging validation and signoff
3. Production canary rollout
4. Full rollout
5. Post-release verification

## Rollback Policy
Immediate rollback if any occurs:
- P1 incident triggered by release
- Clinical command failure rate > 2%
- Data integrity anomaly detected

## Communication Plan
- Pre-release notice to facilities for impactful changes
- Live status updates during rollout
- Post-release summary with outcomes and known issues

## Change Record
Each release stores:
- Scope
- Risk level
- Approvers
- Validation evidence
- Rollback decision if applied

