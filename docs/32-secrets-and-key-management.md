# 32. Secrets and Key Management

## Purpose
Define key lifecycle, secret storage, access control, and emergency procedures.

## Secret Classes
- Service credentials (DB, queues, APIs)
- Signing keys (JWT, webhook signatures)
- Encryption keys (data at rest, backups, mobile sync payloads)

## Secret Storage
- HashiCorp Vault as central secret manager.
- HSM-backed root keys for key encryption keys (KEK).
- No hardcoded secrets in source control or images.

## Key Rotation Policy
- JWT signing keys: every 90 days
- Database encryption keys: every 180 days
- External API credentials: every 90 days or vendor max
- Emergency rotation: immediate upon compromise signal

## Rotation Safety
- Dual-key validation window: 24 hours for JWT verification.
- Versioned key identifiers (`kid`) mandatory.
- Automated rollout with rollback guard.

## Access Control
- Least privilege Vault policies by service identity.
- Human access only via short-lived privileged session + MFA.
- Break-glass access requires dual approval and audit ticket.

## Emergency Key Compromise Runbook
1. Revoke compromised key and dependent sessions.
2. Rotate affected keys and secrets.
3. Re-issue tokens/certs as needed.
4. Audit all accesses during exposure window.
5. Publish incident report and preventive controls.

## Secret Hygiene Controls
- Pre-commit secret scanning
- CI secret scanning on every build
- Runtime detection for accidental secret logging

## Compliance Logging
Every secret read/write/rotate action logs:
- actor/service
- secret path
- timestamp
- reason/change ticket

