-- 0002_domain_extensions.sql — Integrated National Health Platform
-- Adds tables for domains beyond the MVP core (CBHI/mutuelle, B2B supply chain).
-- Apply after 0001_initial.sql:
--   psql "$DATABASE_URL" -f backend/sql/0002_domain_extensions.sql
BEGIN;

-- CBHI / mutuelle -------------------------------------------------------------
CREATE TABLE cbhi_members (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID NOT NULL REFERENCES tenants(id),
    patient_id  UUID REFERENCES patients(id),
    scheme      TEXT NOT NULL DEFAULT 'mutuelle',      -- mutuelle | rama | private
    status      TEXT NOT NULL DEFAULT 'active',
    enrolled_on DATE NOT NULL DEFAULT current_date
);
CREATE INDEX idx_cbhi_members_tenant ON cbhi_members(tenant_id);

CREATE TABLE cbhi_premiums (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id  UUID NOT NULL REFERENCES tenants(id),
    member_id  UUID NOT NULL REFERENCES cbhi_members(id),
    amount     NUMERIC(12,2) NOT NULL,
    period     TEXT,
    paid_on    DATE NOT NULL DEFAULT current_date
);
CREATE INDEX idx_cbhi_premiums_member ON cbhi_premiums(member_id);

-- B2B supply chain ------------------------------------------------------------
CREATE TABLE purchase_orders (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID NOT NULL REFERENCES tenants(id),
    facility_id UUID REFERENCES facilities(id),
    supplier_id UUID REFERENCES tenants(id),
    status      TEXT NOT NULL DEFAULT 'draft',         -- draft | sent | received | cancelled
    total       NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_po_tenant ON purchase_orders(tenant_id, status);

CREATE TABLE purchase_order_lines (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id  UUID NOT NULL REFERENCES tenants(id),
    po_id      UUID NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity   INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL
);

-- Row-level security ----------------------------------------------------------
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['cbhi_members','cbhi_premiums','purchase_orders',
                           'purchase_order_lines'] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t);
    EXECUTE format($p$CREATE POLICY tenant_isolation ON %I
      USING (tenant_id = current_setting('app.tenant_id', true)::uuid)
      WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::uuid);$p$, t);
  END LOOP;
END $$;

COMMIT;
