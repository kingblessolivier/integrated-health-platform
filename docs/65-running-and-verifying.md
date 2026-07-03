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

The data-layer harness bypasses HTTP/JWT, but the API itself **can now be driven with real
tokens** via the auth bootstrap. `FourAxisTokenSerializer` authenticates a Django auth user
and maps it (by username == `nida_id`) to a `staff` row + command bundle.

```bash
cd backend && . .venv/bin/activate
# domain schema (managed=False tables) + auth tables
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f sql/0001_initial.sql
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f sql/0002_domain_extensions.sql
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f sql/0003_regulatory_maternity.sql
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f sql/0004_security.sql
psql "postgresql://inhp:$POSTGRES_PASSWORD@localhost:5432/inhp" -f sql/0005_login_resolver.sql
python manage.py migrate                       # creates django.contrib.auth tables
python manage.py seed_commands                 # the command catalogue
python manage.py bootstrap_user --nida 1199900000000001   # prints a random password

python manage.py runserver
```

> **`0005` matters for login.** `staff` is `FORCE` RLS, but login runs before any tenant
> context exists (`app.tenant_id` is unset), so a plain read returns no rows and the JWT would
> carry **no commands**. The `login_claims()` SECURITY DEFINER function resolves the user's
> claims bypassing RLS. Apply `0005` as a privileged role so the function owner can bypass RLS.

### Troubleshooting: "logged in but no commands / empty dashboard"
The JWT `commands` array is empty. Check, in order:
1. **`0005` applied?** Without it, a non-superuser DB role sees no `staff` at login → no claims.
2. **`seed_commands` run?** If the `commands` catalogue is empty there is nothing to grant.
3. **Login username == `staff.nida_id`?** The token maps the account to its staff by national ID.
4. **`user_commands` rows exist for that staff?** Assigning Django-admin *permissions/groups*
   has no effect — only `user_commands` (staff ↔ command) count. `bootstrap_user` grants them.
Re-running `bootstrap_user --nida <id>` fixes 2–4 in one step; then sign out and back in.

Then exercise the API over HTTP:

```bash
# get a JWT (carries tenant/geo/sensitivity + the command bundle)
TOKEN=$(curl -s localhost:8000/api/v1/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"1199900000000001","password":"<printed-password>"}' | jq -r .access)

# register a patient (PTRG) — and so on through the slice
curl -s localhost:8000/api/v1/patients/ -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"nida_id":"1199900000000002"}'
```

## What's verified vs. not

| Layer | Status |
|---|---|
| Business-logic services (FEFO, split, scrub, state machine, polygon, dosing) | ✅ unit tests |
| Schema + models + services against real Postgres | ✅ `e2e/run_slice.py` (run via Docker/CI) |
| HTTP API + four-axis JWT auth, end-to-end | 🟡 bootstrappable (`migrate` + `bootstrap_user`); needs a live run to confirm |
| Mobile (Flutter) | ⛔ needs a Flutter toolchain to run `flutter test` |
