-- 0005_login_resolver.sql — Integrated National Health Platform
-- Login runs BEFORE any tenant context exists (no JWT yet), so `app.tenant_id` is unset and
-- the FORCE-RLS `staff` table would return zero rows to the token endpoint — leaving the JWT
-- with no commands/scope. This SECURITY DEFINER resolver reads a single staff member's login
-- claims by national ID, bypassing RLS (it runs as the function owner). It returns only that
-- one person's own scope + command bundle, so it does not widen data exposure. Apply after 0004.
BEGIN;

CREATE OR REPLACE FUNCTION login_claims(p_nida text)
RETURNS TABLE (
    staff_id        uuid,
    tenant_id       uuid,
    geo_scope       jsonb,
    max_sensitivity text,
    commands        text[]
)
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT s.id,
           s.tenant_id,
           s.geo_scope,
           s.max_sensitivity::text,
           COALESCE(
             array_agg(uc.command::text ORDER BY uc.command)
               FILTER (WHERE uc.command IS NOT NULL),
             ARRAY[]::text[]
           )
    FROM staff s
    LEFT JOIN user_commands uc ON uc.staff_id = s.id
    WHERE s.nida_id = p_nida
      AND s.status = 'active'
    GROUP BY s.id
    LIMIT 1;
$$;

COMMENT ON FUNCTION login_claims(text) IS
  'Resolve a user''s four-axis login claims by national ID, bypassing RLS for the pre-auth '
  'token endpoint. Owned by a privileged role; returns only the matching staff member''s data.';

COMMIT;
