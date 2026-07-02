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

## Confirmed remaining gaps (tracked, not yet implemented)

| # | Gap | Doc promise | Remediation |
|---|---|---|---|
| 4 | **Only the role + tenant axes are enforced.** `HoldsCommand` checks the command; RLS checks tenant. **Geography and sensitivity axes are not enforced.** | 08: "verifies command + geography + tenant + sensitivity before executing any query" | Add geo/sensitivity checks in `HoldsCommand` (or a query-scoping mixin) using `geo_scope` / `max_sensitivity` claims; add negative tests. |
| 5 | **Consent is not enforced.** | 08: consent enforced *in addition to* authorisation | Implement a `ConsentPolicy` gate on patient-record reads (docs/56 already models it). |
| 6 | On **403**, the server does not terminate the session / blacklist the JWT / log the event (the frontend logs out, but the token stays valid). | 08: out-of-scope → 403 + terminate + blacklist + log | Add a Redis JWT blacklist + audit entry in the permission-denied path (ties into `SELK`). |
| 7 | JWT default **HS256**; MFA not implemented. | 08: **RS256** (key in HSM), MFA for clinical/admin | Configure RS256 keys for staging/prod; add an MFA step to the token flow. |
| 8 | **PHI field-level encryption** and TLS/mTLS are infra-level, not in app code yet. | 08: AES-256 at rest, app-layer PHI encryption, TLS 1.3, mTLS | Add field encryption for PHI columns; terminate TLS/mTLS at the mesh/ingress. |

## Verified already correct
- **Audit chain** (`apps/audit/services.py`) chains each entry with SHA-256 over the previous
  hash; `audit_log` is append-only (`REVOKE UPDATE, DELETE`) and excluded from RLS so the
  chain is globally sequential — matches docs 08/34.
- Every command endpoint writes an audit entry; commands are the unit of access (docs 04).

## Priority before production
1–3 done. **#4, #5, #6 are the must-do items before real PHI** (they are the core of the
documented four-axis + consent model). #7/#8 are infra/config for the staging/prod rollout.
