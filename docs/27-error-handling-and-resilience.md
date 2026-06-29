# 27. Error Handling and Resilience Patterns

## Purpose
Define how the platform behaves when dependencies fail, latency spikes, or partial outages occur, while preserving patient safety and core continuity of care.

## Resilience Principles
1. **Patient safety first**: clinical capture and emergency workflows remain available in degraded mode.
2. **Fail fast with clear reason**: short timeouts and explicit error classes.
3. **Graceful degradation**: reduce features, not total availability.
4. **Observable failure**: every degraded mode emits metrics, traces, and audit events.
5. **Recover automatically when safe**: controlled retries, circuit half-open probes, idempotent replay.

## Standard Error Taxonomy
- `VALIDATION_ERROR` (4xx): invalid payloads, schema mismatch.
- `AUTHN_ERROR` (401): token/session invalid.
- `AUTHZ_ERROR` (403): command denied by policy.
- `CONFLICT_ERROR` (409): optimistic lock/sync collision.
- `DEPENDENCY_ERROR` (424/503): upstream system unavailable.
- `TIMEOUT_ERROR` (504): response exceeded timeout budget.
- `RATE_LIMITED` (429): quota exceeded.
- `INTERNAL_ERROR` (500): unexpected failure.

All APIs return:
- `error_code`
- `message` (user-safe)
- `correlation_id`
- `retryable` (boolean)
- `next_action` (optional UI hint)

## Timeout and Retry Policy (Default)
- Internal service-to-service timeout: **2s**
- External dependency timeout: **3s**
- Read retries: **max 2** with exponential backoff (100ms, 300ms) + jitter
- Write retries: only for **idempotent** commands with idempotency key
- Global request deadline: **8s**

## Circuit Breaker Baseline
Per external integration (NIDA, DHIS2, RSSB, EBM, KWIVUZA, SAMU):
- Open threshold: **50% failures over 20 requests in 60s**
- Open duration: **30s**
- Half-open probes: **5 requests**
- Close condition: **>= 80% success in probes**

## Queue Backpressure and Limits
- Command queue max depth per tenant: **10,000**
- Dead-letter queue after **5 attempts**
- Priority classes:
  1. Emergency/critical care
  2. Clinical documentation
  3. Billing/reporting
  4. Analytics/export

When depth > 80%: start rejecting low-priority tasks with 429 + Retry-After.

## Graceful Degradation Matrix
### NIDA unavailable
- Registration using NIDA verification switches to **deferred verification mode**.
- User sees: “National ID verification temporarily unavailable; patient can be provisionally registered.”
- Required follow-up task generated for verification within 24h.

### DHIS2 unavailable
- Reporting events buffered locally in durable queue.
- Retry scheduler flushes when dependency recovers.
- Dashboard marks indicators as "stale" with last successful sync timestamp.

### RSSB unavailable
- Claims submitted to outbox; status shown as "pending payer sync".
- No duplicate submission allowed without idempotency key.

### SMS provider unavailable
- OTP fallback to TOTP or voice channel when configured.
- Non-critical notifications delayed and retried.

## Idempotency Requirements
Mandatory for:
- Patient registration command
- Claim submission command
- Payment settlement command
- Referral transfer command

Idempotency key format: `tenant_id:command_type:client_request_id`.
Retention: 72h.

## Partial Failure Handling
- Use saga compensation for multi-step workflows.
- Persist command intent before side effects.
- Mark step-level status with resumable checkpoints.

## User Experience in Failure States
- Always show `correlation_id` on error dialogs.
- Provide explicit action: retry now, save offline, or contact support.
- Prevent silent data loss by autosaving drafts every 10s.

## Operational Runbook (Quick)
1. Check circuit breaker state dashboard.
2. Confirm dependency health and latency.
3. If queue lag > threshold, apply backpressure policy.
4. Verify DLQ growth and replay only validated events.
5. Post incident note in incident channel with timeline and impact.

## SLO Alignment
- Dependency-induced failed clinical commands < 0.5% per day.
- Recovery from transient upstream outage < 10 minutes (P95).

