# 34. Audit Chain Integrity and Verification

## Purpose
Define tamper-evident audit log integrity controls and recovery procedures.

## Chain Model
- Each audit record includes previous-hash pointer.
- Hash algorithm: SHA-256.
- Daily anchor digest signed by HSM-backed key.

## Verification Schedule
- Continuous streaming validation for append operations.
- Full chain verification: every 6 hours.
- Cross-store checksum comparison: daily.

## Tamper Detection Triggers
- Hash mismatch
- Missing sequence number
- Duplicate sequence insertion
- Signature verification failure

Any trigger creates a P1 security incident.

## Recovery Procedure
1. Freeze audit ingestion cursor.
2. Snapshot current chain state for forensics.
3. Reconstruct from last known valid anchor.
4. Replay verified event source logs.
5. Mark reconstructed segment with incident metadata.

## Retention
- Hot audit index: 90 days
- Immutable archive: 7 years (or legal requirement)

## Export Format
- JSONL with signatures
- CSV (redacted) for operational review
- Signed evidence bundle for compliance audits

