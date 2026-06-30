# 65 — Running & Verifying Locally

How to actually run the platform and prove the Clinical Slice works end-to-end. This is the
verification path referenced throughout the roadmap ([64](64-mvp-scope-and-roadmap.md)).

## Unit tests (no services needed)

```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
ruff check . && pytest        # 35 tests
```

## Data-layer end-to-end (real Postgres)

Proves the schema + models + business-logic services agree against a live database:
register → encounter → diagnosis → prescription → **FEFO dispense** → POS checkout → claim
scrub/approve, asserting the key invariants (FEFO picks the earliest in-date batch, stock
decrements, the payment split sums to the total, the claim reaches `approved`).

```bash
# 1. start Postgres (TimescaleDB + PostGIS) — applies the schema on first boot
cp .env.example .env            # set POSTGRES_PASSWORD
docker compose up -d db

# 2. (if the volume already existed) apply the schema manually
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f backend/sql/0001_initial.sql

# 3. run the harness
cd backend && python -m e2e.run_slice
# -> "E2E PASS: register -> ... -> claim approved"
```

In CI this runs automatically via **`.github/workflows/e2e.yml`** (a TimescaleDB service +
schema apply + `python -m e2e.run_slice`) — once GitHub Actions is enabled on the repo.

## Known gap — HTTP + JWT end-to-end

The data-layer harness deliberately **bypasses the HTTP/JWT layer**. A full
`curl`-against-the-API run isn't possible yet because authentication isn't bootstrapped:

- `FourAxisTokenSerializer` authenticates a Django auth user and maps it to a `staff` row,
  but `backend/sql/0001_initial.sql` does not create `django.contrib.auth` tables and there
  is no custom-user migration.

**Follow-up to close it:** either add the `contrib.auth`/`contenttypes` migrations (or a
custom user model) to the migration path, add a `createsuperuser`-style bootstrap that links
a user to a `staff` row + command bundle, then the API can issue real JWTs and the same slice
can be exercised over HTTP. Tracked as the next verification increment.

## What's verified vs. not

| Layer | Status |
|---|---|
| Business-logic services (FEFO, split, scrub, state machine, polygon, dosing) | ✅ unit tests |
| Schema + models + services against real Postgres | ✅ `e2e/run_slice.py` (run via Docker/CI) |
| HTTP API + four-axis JWT auth, end-to-end | ⛔ blocked on auth bootstrap (above) |
| Mobile (Flutter) | ⛔ needs a Flutter toolchain to run `flutter test` |
