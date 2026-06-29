# 39. Mobile App Security

## Purpose
Define mobile security baseline for clinical apps operating in variable connectivity environments.

## Controls
- Certificate pinning enabled for API domains.
- TLS 1.3 required.
- Local storage encrypted via SQLCipher.
- Keystore-backed key material, non-exportable.

## Pin Rotation
- Publish next pin before cert rollover window.
- Support dual-pin validation during transition.
- If pin mismatch spikes, activate controlled fallback plan and forced update.

## App Integrity
- Device attestation required for high-risk operations.
- Root/jailbreak detection with risk-based policy.
- Tampered app binaries blocked from privileged actions.

## Session Security
- Short-lived access tokens + refresh token rotation.
- Inactivity lock after 2 minutes for shared devices.
- Optional biometric unlock per policy.

## Incident Response
If compromised app build detected:
1. Revoke affected app signing trust.
2. Force minimum safe app version.
3. Notify facilities and provide update guidance.

