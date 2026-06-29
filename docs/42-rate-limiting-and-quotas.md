# 42. Rate Limiting and Quota Management

## Purpose
Protect platform stability and fair usage with explicit limits and backpressure behavior.

## Default API Limits
- Per user: 600 requests/min
- Per facility: 10,000 requests/min
- Burst allowance: 2x for 30 seconds

## Command Limits
- Bulk patient import: max 5,000 records/job
- FHIR bundle submit: max 500 resources/request
- Claim submit batch: max 1,000 claims/job

## Response Behavior
- Exceeding limits returns `429` with `Retry-After`.
- Include quota headers:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Priority and Fairness
- Emergency workflows get reserved capacity pool.
- Non-critical analytics/export throttled first during load spikes.

## Provider-Specific Throttling
- SMS/notification gateways have dedicated dispatch queues.
- Respect provider throughput contracts and retry windows.

## Monitoring
- Alert when 429 ratio > 2% for 10m.
- Dashboard by tenant/facility for quota pressure.

