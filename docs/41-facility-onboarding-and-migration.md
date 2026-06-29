# 41. Facility Onboarding and Data Migration

## Purpose
Define safe onboarding of facilities and migration from legacy systems with rollback capability.

## Onboarding Phases
1. Pre-assessment
2. Data mapping and cleansing
3. Pilot migration
4. Parallel run
5. Cutover
6. Hypercare

## Pre-Go-Live Checklist
- User roster validated
- Device readiness confirmed
- Connectivity and offline plan validated
- Integration credentials provisioned
- Training completed and attendance recorded

## Migration Controls
- Source-to-target mapping specification approved.
- Dry-run migration with reconciliation report.
- Data quality thresholds must pass before cutover.

## Parallel Run
- Duration: 2–4 weeks (facility dependent)
- Compare critical metrics between legacy and new system daily.
- Escalate divergences above agreed tolerance.

## Cutover Runbook
1. Freeze legacy write window.
2. Execute final delta migration.
3. Validate record counts and critical patient samples.
4. Switch operational users to new platform.
5. Monitor with hypercare command center for 72h.

## Rollback Criteria
- Critical clinical workflow failure > 30 minutes
- Data integrity mismatch beyond tolerance
- Safety risk declared by clinical lead

## Post-Go-Live
- Daily issue triage for first 14 days.
- Formal signoff after stabilization checklist.

