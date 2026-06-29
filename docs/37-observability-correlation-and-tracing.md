# 37. Observability, Correlation, and Tracing

## Purpose
Provide traceability across services and workflows with consistent observability standards.

## Telemetry Standards
- Metrics: Prometheus
- Traces: OpenTelemetry + Jaeger
- Logs: structured JSON to centralized index

## Correlation ID Policy
- Ingress assigns `correlation_id` if absent.
- Propagate across HTTP, async messages, and background jobs.
- Include correlation_id in every error response and audit event.

## Required Log Fields
- timestamp
- service_name
- environment
- tenant_id (if applicable)
- actor_id (if applicable)
- correlation_id
- severity
- event_type

## PII/PHI Redaction
- Never log raw identifiers, diagnosis text, or full payloads containing PHI.
- Use tokenized references for patient entities.
- Enforce redaction middleware in all services.

## Trace Coverage Targets
- 100% of critical commands sampled
- >= 20% of non-critical traffic sampled baseline
- Adaptive upsampling during incidents

## Dashboards
- Service health and golden signals
- End-to-end clinical workflow trace board
- Integration dependency latency board
- Queue and retry health board

## Retention
- Logs: 180 days hot, 1 year archive (redacted)
- Traces: 30 days hot
- Metrics: 13 months rollup

