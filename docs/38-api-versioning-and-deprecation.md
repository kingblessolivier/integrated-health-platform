# 38. API Versioning and Deprecation Policy

## Purpose
Provide backward-compatible API evolution with controlled breaking-change rollout.

## Versioning Model
- URI versioning for public APIs: `/api/v1`, `/api/v2`
- Event schema versioning via explicit `schema_version` field.
- FHIR profile versions tracked and published per release.

## Compatibility Rules
- Minor releases cannot remove or rename existing fields.
- Breaking changes require new major version.
- Deprecated fields remain supported for minimum 12 months.

## Deprecation Lifecycle
1. Announce deprecation with migration guidance.
2. Emit warning headers and logs.
3. Track consumer adoption.
4. Enforce sunset date with approved governance signoff.

## Mobile Client Strategy
- Support N-1 mobile app major version for 12 months.
- Feature flags for gradual rollout.
- Kill-switch for incompatible endpoints if safety risk identified.

## FHIR and Integration Changes
- Maintain compatibility matrix across DHIS2/eIDSR/RSSB adapters.
- Validate mappings in conformance test suite before release.

