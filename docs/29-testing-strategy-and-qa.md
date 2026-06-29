# 29. Testing Strategy and Quality Assurance

## Purpose
Establish end-to-end quality controls across functional correctness, interoperability, security, resilience, and performance.

## Test Pyramid
1. Unit tests
2. Contract tests
3. Integration tests
4. End-to-end clinical workflow tests
5. Non-functional tests (load, chaos, security)

## Mandatory Quality Gates (CI)
- Unit coverage >= 85% for core clinical services
- 100% pass for critical command contracts
- Zero high-severity static-analysis findings
- SBOM generation + dependency vulnerability scan

## Integration Smoke Suite (per deploy)
- NIDA identity verification flow
- DHIS2 reporting push
- RSSB claim submission
- EBM medicine availability query
- SAMU dispatch handoff

Any smoke failure blocks production deployment.

## Load Testing
### Baseline workload
- 10,000 concurrent active sessions
- 1,500 req/s mixed read/write
- Peak emergency spike: 2x for 5 minutes

### Targets
- P95 API latency < 500ms (core read)
- P95 command completion < 2s (clinical writes)
- Error rate < 1% under baseline

## Chaos Testing
Monthly scenarios:
- Kill one database replica
- Introduce 20% packet loss to external integrations
- Force message queue node restart
- Simulate DNS failure for one upstream API

Success criterion: no critical data loss, core workflows remain available.

## Security Testing
- Quarterly penetration testing (external + internal)
- Monthly privilege escalation regression tests
- Secrets scanning on every push
- Session fixation and JWT replay tests

## FHIR Conformance Matrix
Maintain tested versions and profile compatibility for:
- FHIR R4 profiles in platform
- DHIS2 mapping profile version
- eIDSR mapping profile version

Every release must publish a matrix artifact.

## Mobile Sync QA
- Offline create/update/delete stress tests
- Conflict merge scenarios by role (CHW/Nurse/Doctor)
- Device storage corruption recovery tests
- Upgrade tests for schema migrations

## UAT and Clinical Validation
- Role-based scripted scenarios per facility type
- Sign-off by clinical governance before national rollout
- Critical-path checklist required for go-live

## Release Criteria
A release is promotable only when:
1. All CI gates pass
2. Smoke suite passes in staging
3. Load regression delta < 10% from previous stable baseline
4. Security gates pass with no open critical findings

