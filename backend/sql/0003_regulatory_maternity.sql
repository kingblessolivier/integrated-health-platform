-- 0003_regulatory_maternity.sql — Integrated National Health Platform
-- Adds regulatory (Rwanda FDA) and maternity tables. Apply after 0002.
BEGIN;

-- Regulatory (product-scoped, national — not tenant-isolated) ------------------
CREATE TABLE drug_registrations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id  UUID REFERENCES products(id),
    importer    TEXT,
    status      TEXT NOT NULL DEFAULT 'registered',   -- registered | suspended | recalled
    expires_on  DATE
);
CREATE TABLE adverse_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id  UUID REFERENCES products(id),
    description TEXT NOT NULL,
    severity    TEXT NOT NULL DEFAULT 'mild',         -- mild | moderate | severe
    reported_on DATE NOT NULL DEFAULT current_date
);

-- Maternity (tenant-scoped) ---------------------------------------------------
CREATE TABLE deliveries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id    UUID NOT NULL REFERENCES tenants(id),
    encounter_id UUID REFERENCES encounters(id),
    patient_id   UUID REFERENCES patients(id),
    outcome      TEXT NOT NULL DEFAULT 'live_birth',
    delivered_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE births (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id    UUID NOT NULL REFERENCES tenants(id),
    delivery_id  UUID NOT NULL REFERENCES deliveries(id),
    sex          TEXT,
    weight_grams INTEGER,
    registered   BOOLEAN NOT NULL DEFAULT false
);

DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['deliveries','births'] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY;', t);
    EXECUTE format($p$CREATE POLICY tenant_isolation ON %I
      USING (tenant_id = current_setting('app.tenant_id', true)::uuid)
      WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::uuid);$p$, t);
  END LOOP;
END $$;

COMMIT;
