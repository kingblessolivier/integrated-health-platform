# 28. Mobile Sync and Conflict Resolution

## Purpose
Define the offline-first sync protocol, conflict handling algorithm, and operational guarantees for mobile clients used in low-connectivity settings.

## Sync Model
- **Local-first writes** to encrypted device store.
- **Operation log (oplog)** with monotonic sequence numbers.
- **Server reconciliation** using version vectors per entity.

## Data Structures
Each mutation carries:
- `entity_id`
- `entity_type`
- `op_type` (create/update/delete)
- `client_op_id` (UUID)
- `base_version`
- `actor_id`
- `timestamp_client`
- `patch` (JSON Patch)

Server assigns:
- `server_version`
- `applied_at`
- `conflict_flag`

## Sync Protocol
1. Client authenticates and sends last acknowledged server checkpoint.
2. Client uploads pending oplog batch (max 200 ops/request).
3. Server validates schema + authorization + base version.
4. Server applies non-conflicting ops transactionally.
5. Server returns conflict set + authoritative state delta.
6. Client merges, prompts user where required, and acknowledges checkpoint.

## Conflict Types
1. **Field-level non-overlapping updates** → auto-merge.
2. **Same-field concurrent updates** → policy-driven resolution.
3. **Delete vs update** → block and require user decision.
4. **Reference integrity conflict** (e.g., parent missing) → deferred retry bucket.

## Resolution Policy
- Default: **clinical-safe merge** (not naive last-write-wins).
- Critical fields (diagnosis, allergies, medication dosage): **manual resolution required**.
- Non-critical metadata (notes tags, UI state): **latest timestamp wins**.
- Deletions require supervisor role if conflicting with newer clinical entry.

## Resolution UX
When manual conflict exists:
- Show side-by-side: "Local change" vs "Server change"
- Highlight changed fields
- Require explicit selection and reason code
- Log to audit trail with `resolver_user_id`

## Ordering and Prioritization
Upload priority:
1. Emergency encounters
2. Medication administrations
3. Lab/diagnostic updates
4. Administrative updates

Within priority class, order by `timestamp_client`, then `client_op_id`.

## Integrity and Safety
- SHA-256 checksum per batch.
- Replay protection using `client_op_id` dedupe table (72h).
- Partial batch failure returns per-op status; successful ops are not replayed.

## Resume After Partial Failure
- Client stores `last_successful_op_index`.
- Retry starts from next failed op.
- Exponential backoff with jitter up to 5m max interval.

## Device Security Controls
- Local SQLite encrypted (SQLCipher AES-256).
- Key material wrapped via platform keystore.
- App-level lock timeout: 2 minutes inactivity.

## Testing Requirements
- Simulate two clinicians editing same encounter offline.
- Simulate long offline window (7 days) with schema evolution.
- Simulate duplicate sends and packet loss.
- Validate no silent overwrite of critical clinical fields.

## Performance Targets
- 95% of sync batches complete < 3s on 4G.
- Conflict rate < 2% of total ops/day.
- Manual conflict resolution completion < 15 min P95.

