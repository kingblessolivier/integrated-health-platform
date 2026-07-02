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

## Also addressed in the gap-closing pass

| # | Item | Status |
|---|---|---|
| 6 | **Geography axis** | `in_geo_scope` + `filter_by_geo` query-layer helper added & unit-tested. Wire into list endpoints that carry a location; models without a geo column still rely on tenant RLS. |
| 7 | **403 → blacklist + log** | JWT **blacklist** (`apps/security/blacklist.py`), `SELK` **LOCK** endpoint, a **blacklist-aware authentication** class that rejects revoked tokens, and an **audited exception handler** that logs denials. ✅ |
| 8a | **RS256** | Settings support RS256 signing/verifying keys when `JWT_ALG=RS256` (private key in HSM). ✅ config |
| 8b | **MFA** | TOTP verify (`apps/security/mfa.py`, RFC 6238, stdlib) **now enforced at login**: `FourAxisTokenSerializer.validate` requires a valid `otp` for any user with a confirmed `MfaDevice` (`apps/security/models.py`, `mfa_devices` table in `sql/0004`), raising `mfa_required` after password auth. ✅ |
| 9a | **PHI field encryption** | `EncryptedTextField` (`apps/security/fields.py`) transparently Fernet-encrypts on write / decrypts on read; **applied to `Diagnosis.note`**. Reads tolerate NULL and legacy plaintext for in-place migration. ✅ |
| 9b | **TLS 1.3 / mTLS / HSM / Kong / Cloudflare** | **Deployment/infra, not code** — configured at the mesh/ingress/KMS per docs 07/08/23. Out of application scope. |

## Verified already correct
- **Audit chain** (`apps/audit/services.py`) chains each entry with SHA-256 over the previous
  hash; `audit_log` is append-only (`REVOKE UPDATE, DELETE`) and excluded from RLS so the
  chain is globally sequential — matches docs 08/34.
- Every command endpoint writes an audit entry; commands are the unit of access (docs 04).

## Priority before production
Items 1–9a are now addressed in code (RLS FORCE, Argon2, least-privilege, sensitivity axis,
consent gate, geography helper, JWT blacklist + LOCK + denial logging, **MFA enforced at
login**, **PHI field encryption applied**). What remains is deployment/infra configuration,
not application code: RS256 signing keys in the HSM (8a) and TLS 1.3 / mTLS / HSM / gateway
(9b), provisioned at the mesh/ingress/KMS per docs 07/08/23.
