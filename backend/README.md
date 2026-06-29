# Backend — Integrated National Health Platform API

Django + DRF skeleton implementing the command-driven, four-axis API (docs
[04](../docs/04-access-control-model.md), [49](../docs/49-api-contract.md)).

## Layout
```
config/            settings, urls, wsgi/asgi
apps/
  common/          TenantContextMiddleware (sets RLS session vars)
  accounts/        Command/Staff/UserCommand models + HoldsCommand permission
  audit/           SHA-256 audit-chain append service (docs/34)
  patients/        sample command-bound app (PTRG/PTSR/PTVW) with NIDA stub
sql/0001_initial.sql   canonical, runnable schema (mirrors docs/48)
```

## Run (local)
```bash
cp .env.example .env
pip install -r requirements.txt
# apply the canonical schema (owns the DDL; ORM models use managed=False)
psql "postgresql://inhp:inhp@localhost:5432/inhp" -f sql/0001_initial.sql
python manage.py runserver
```

Or use the repo-root `docker-compose.yml` (Postgres + Redis + API).

## Notes
- The SQL migration owns the DDL (RLS, partitioning, TimescaleDB); ORM models mirror the
  subset the API touches (`managed = False`).
- Swap JWT to **RS256** with HSM/Vault-managed keys before production (docs/32).
- Replace the NIDA/EBM stubs with real adapters behind circuit breakers (docs/09).
