# 36. Payment and Financial Controls

## Purpose
Define secure payment processing, reconciliation, and exception handling controls.

## Payment Principles
- Ledger is source of truth.
- Every settlement event must be authenticated and idempotent.
- Financial actions are fully auditable.

## Webhook Security
- HMAC signature validation required.
- Timestamp tolerance <= 5 minutes.
- Replay protection via nonce cache (24h).
- Reject unsigned or stale callbacks.

## Reconciliation Process
- Automated reconciliation every hour.
- Daily close reconciliation at 23:30 CAT.
- Compare external provider settlements to internal ledger entries.

## Exception Handling
If mismatch detected:
1. Mark transaction as `RECONCILIATION_EXCEPTION`.
2. Hold downstream disbursement.
3. Open finance investigation ticket.
4. Resolve via approved adjustment command.

## Approval Controls
- Transactions above threshold require dual authorization.
- Threshold values configurable by governance policy.

## Dispute Workflow
- Register dispute with reason and evidence.
- Freeze disputed amount state.
- Track SLA for dispute resolution.

## Reporting
- Daily settlement summary
- Exception aging report
- Reversed/refunded transaction report

