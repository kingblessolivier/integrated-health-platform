# 51 — Mobile & Offline Architecture

The Flutter apps (CHW, patient, ambulance tablet) must keep working with **no network** and
reconcile cleanly when connectivity returns. This is the concrete contract behind the policy
in [28 — Mobile Sync and Conflict Resolution](28-mobile-sync-and-conflict-resolution.md).

## Stack

- **Flutter (Dart)**, one codebase for Android/iOS + ruggedised tablet.
- Local store: **Hive** (CHW iCCM decision tables, lightweight KV) and **SQLite** (`drift`)
  for the relational op-log and cached records.
- iCCM decision trees and the **GPS polygon check run entirely on-device** (offline).
- Security: see *Mobile security* below and [39 — Mobile App Security](39-mobile-app-security.md).

## Project structure

```
lib/
├── core/            # theme tokens (doc 05), config, di
├── data/
│   ├── local/       # drift db, hive boxes, op_log dao
│   ├── remote/      # api client (doc 49), auth, retry
│   └── sync/        # sync engine + conflict resolver
├── domain/          # entities, use-cases (register, diagnose, dispense)
└── features/        # chw / patient / ambulance UIs
```

## Operation-log schema (local SQLite)

Every offline write is an append to a local op-log, not a direct mutation — the log is the
unit of sync.

```sql
CREATE TABLE op_log (
  client_op_id   TEXT PRIMARY KEY,   -- UUID, also the API Idempotency-Key
  entity_type    TEXT NOT NULL,      -- patient | encounter | observation | dispense …
  entity_id      TEXT NOT NULL,
  op_type        TEXT NOT NULL,      -- create | update | delete
  base_version   INTEGER,            -- server version the change was based on
  patch          TEXT NOT NULL,      -- JSON Merge/RFC-6902 patch
  command        TEXT NOT NULL,      -- the command code (e.g. RXDP)
  created_at     TEXT NOT NULL,      -- ISO8601, device clock
  status         TEXT NOT NULL       -- pending | syncing | synced | conflict
);
```

## Sync engine

```
on connectivity-restored OR periodic tick:
  1. pull: GET changes since last_sync_cursor → upsert local cache
  2. push: for each op_log row where status = pending (in created_at order):
       POST with Idempotency-Key = client_op_id
       200/201 → status = synced
       409 (version mismatch) → status = conflict  → resolver
       5xx / offline → leave pending, exponential backoff
  3. advance last_sync_cursor
```

- **Idempotency-Key = `client_op_id`** makes replay safe: a retried op never double-applies
  server-side (doc 49).
- A persistent **sync-status banner** reflects the queue: green (synced) / amber
  (offline-autonomous) / red (sync error) — using the corrected amber rules in doc 05
  (dark text on amber, never white).

## Conflict resolution

Most writes are **non-overlapping** (different patients/fields) and auto-merge. Genuine
conflicts on the same field surface to the user — never silently overwrite:

```
conflict (same field, divergent values):
  1. show side-by-side: "Your version"  vs  "Server version" (with author + time)
  2. user picks one (or merges) and gives a short reason
  3. push resolution as a new op_log entry
  4. audit-chain records the resolution (actor, command, both values, reason)
```

Last-write-wins is used **only** for low-risk, non-clinical fields; clinical data always goes
to human resolution.

## Mobile security

- **Encrypted local storage** (SQLCipher / encrypted Hive); device keystore for keys.
- **TLS 1.3 + certificate pinning** — a MITM is detected and the connection refused (doc 19/39).
- Short-lived JWT with refresh; on logout/termination all local tokens are wiped.
- No PHI is logged; crash reports are scrubbed.
- Offline data is purged on remote `LOCK` of the account once the device next reaches network.

## Offline-capable safety checks

- iCCM diagnostic flow, dose-by-age/weight calculation, and the **GPS village-polygon check**
  use locally cached decision/boundary tables, so a CHW is never blocked by lack of signal.
- The virtual health kit is decremented locally and reconciled on sync.
