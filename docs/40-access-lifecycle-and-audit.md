# 40. Access Lifecycle and Permission Audit

## Purpose
Define joiner/mover/leaver lifecycle controls and periodic access recertification.

## Lifecycle Stages
1. Provisioning (joiner)
2. Role/facility transfer (mover)
3. Revocation (leaver)

## Provisioning Controls
- Access granted only from approved role templates.
- Effective-dated activation and expiry where possible.

## Transfer Controls (Mover)
- Remove old facility permissions before activating new facility scope.
- Re-issue context-bound privileges and verify least privilege.

## Revocation Controls (Leaver)
- Immediate disable on termination event.
- Token/session invalidation within 5 minutes.
- API keys and device sessions revoked same day.

## Recertification
- Quarterly manager review of active access.
- Detect stale privileged accounts (unused > 45 days).
- Exception register with remediation deadlines.

## Audit Reporting
Monthly reports:
- New privileged grants
- Revocations completed within SLA
- Stale access exceptions

