# 66 — Security Review (code vs. documented model)

An honest audit of the implementation against the documented security model
([04](04-access-control-model.md) · [08](08-security-and-cryptography.md) ·
[34](34-audit-chain-integrity.md) · [35](35-multi-tenancy-and-data-isolation.md)). Records
what is enforced, what was fixed, and what is still a gap before `dev → main`.

## Fixed in this pass

| # | Finding | Doc promise | Fix |
|---|---|---|---|
| 1 | **RLS was `ENABLE`d but not `FORCE`d** — Postgres exempts the table owner from RLS, and the app connects as owner, so tenant isolation silently did not hold. | 35 §Database Isolation: "RLS enforced on tenant tables" | Added `FORCE ROW LEVEL SECURITY` to every tenant table across `0001`/`0002`/`0003`; `bootstrap_user` now sets `app.tenant_id` before writing. |
| 2 | Passwords used Django's default **PBKDF2**. | 08: **Argon2id** | Set `PASSWORD_HASHERS` to Argon2 first; added `argon2-cffi`. |
| 3 | `bootstrap_user` created a **Django superuser**. | 08: least privilege | Now a normal user; all access comes from the command bundle. |
| 4 | **Sensitivity axis** unenforced. | 08: four-axis (sensitivity) | `HoldsCommand` now enforces a view's `min_sensitivity` against the JWT `max_sensitivity`; individual-PHI views (patients, encounters, diagnoses, FHIR export) marked `individual`. |
| 5 | **Consent** unenforced. | 08: consent in addition to authz | `consent_permits` gate wired into patient-record reads (`PatientDetail`) — a revoked actor gets 403. |

## Confirmed remaining gaps (tracked, not yet implemented)

| # | Gap | Doc promise | Remediation |
|---|---|---|---|
| 6 | **Geography axis**: `in_geo_scope` helper exists and is unit-tested, but it is **not yet applied at the query layer** for every list endpoint (they rely on tenant RLS only). | 08: geography verified before every query | Apply `in_geo_scope` (or a geo-scoping queryset mixin) to district/facility list endpoints; add negative tests. |
| 7 | On **403**, the server does not terminate the session / blacklist the JWT / log the event (the frontend logs out, but the token stays valid). | 08: out-of-scope → 403 + terminate + blacklist + log | Add a Redis JWT blacklist + audit entry in the permission-denied path (ties into `SELK`). |
| 8 | JWT default **HS256**; MFA not implemented. | 08: **RS256** (key in HSM), MFA for clinical/admin | Configure RS256 keys for staging/prod; add an MFA step to the token flow. |
| 9 | **PHI field-level encryption** and TLS/mTLS are infra-level, not in app code yet. | 08: AES-256 at rest, app-layer PHI encryption, TLS 1.3, mTLS | Add field encryption for PHI columns; terminate TLS/mTLS at the mesh/ingress. |

## Verified already correct
- **Audit chain** (`apps/audit/services.py`) chains each entry with SHA-256 over the previous
  hash; `audit_log` is append-only (`REVOKE UPDATE, DELETE`) and excluded from RLS so the
  chain is globally sequential — matches docs 08/34.
- Every command endpoint writes an audit entry; commands are the unit of access (docs 04).

## Priority before production
Items 1–5 done (RLS FORCE, Argon2, least-privilege, sensitivity axis, consent gate).
**#6 (geography at the query layer) and #7 (403 blacklist/log) are the remaining core items**
before real PHI. #8/#9 (RS256+MFA, PHI field encryption + TLS/mTLS) are infra/config for the
staging/prod rollout.
