# 33. Data Residency and Compliance Enforcement

## Purpose
Ensure technical enforcement of national data residency and healthcare compliance obligations.

## Residency Requirement
All production PHI/PII data, backups, and analytics datasets must remain within approved Rwanda-hosted facilities.

## Technical Enforcement
- Region-locked infrastructure policies.
- Egress firewall deny-by-default to non-approved regions.
- Object storage replication restricted to approved in-country sites.
- CDN configuration excludes PHI payload caching.

## Data Classification
- Tier 1: PHI/PII (strict residency + encryption)
- Tier 2: Operational metadata (restricted export)
- Tier 3: Public/non-sensitive content

## Compliance Controls
- Encryption at rest (AES-256) and in transit (TLS 1.3)
- Access logging for all PHI reads
- Consent and purpose-of-use checks on data access commands

## Audit Evidence
Quarterly compliance pack includes:
- Hosting location attestation
- Backup location report
- Access log samples and anomaly summary
- Data export register

## Third-Party Services
Any external processor must document:
- Data categories processed
- Physical processing location
- Retention and deletion policy
- Contractual compliance commitments

## Incident Handling
If residency breach suspected:
1. Block external egress path.
2. Identify affected dataset and time window.
3. Notify governance and compliance authority.
4. Complete forensic review and remediation.

