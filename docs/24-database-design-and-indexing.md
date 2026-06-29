# 24 — Database Design & Indexing

## Core design principles

- **Multi-tenant by design:** every row carrying patient or organisational data has a
  `tenant_id` and `facility_id`, enforced by PostgreSQL **row-level security (RLS)**.
- **ACID compliance:** a sale and a stock decrement always succeed or fail together.
- **Temporal data:** audit-sensitive tables are append-only; updates are new rows with a
  `valid_from` / `valid_to` range (**bitemporal** design).
- **Referential integrity** enforced at the database level, not just in application code.

## Key tables & indexes

| Table | Indexing strategy |
|---|---|
| `patients` | B-tree on `(nida_id)` for sub-millisecond identity lookup; composite `(tenant_id, patient_id)` |
| `encounters` | Composite `(patient_id, encounter_date DESC)` for history; `(facility_id, status)` for queues; BRIN on `(created_at)` for time-range reporting |
| `prescriptions` | B-tree on `(code)` for SMS-code lookup at the pharmacy counter |
| `stock_items` | Composite `(facility_id, product_id, expiry_date ASC)` for FEFO selection; partial index on low-stock condition |
| `transactions` | Composite `(facility_id, transaction_date)` for daily reconciliation; partial index on `status = 'pending'` |
| `audit_log` | Append-only; indexed on `(actor_id, timestamp)` and `(resource_type, resource_id)`; `hash_chain` column verified on schedule |
| `diagnosis_codes` | GiST trigram index for fast ICD code/description lookup by typing |
| `locations` (geographic) | PostGIS GiST index on geometry columns for village-polygon membership and ambulance proximity |
| `vitals_stream` | TimescaleDB hypertable partitioned by time; automatic chunk compression after 30 days |

## Partitioning & optimisation

- `encounters` and `transactions` are **range-partitioned by month**; older partitions move
  to slower storage automatically.
- `stock_items` is **hash-partitioned by `facility_id`** to distribute load across nodes.
- **Materialised views** serve expensive aggregate dashboard queries, refreshed on schedule
  rather than computed on demand.
- Slow-query logging is enabled; queries exceeding **200 ms** are flagged for index review.
- PgBouncer pools connections in **transaction mode** to maximise throughput under load.

## Backup & recovery

- **WAL archiving** enabled; point-in-time recovery to any second in the last **30 days**.
- Daily full backups encrypted with AES-256 and stored in a separate location within Rwanda.
- Backup restoration tested monthly; **recovery time objective (RTO) under 30 minutes**.
