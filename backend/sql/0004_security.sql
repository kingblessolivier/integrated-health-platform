-- 0004_security.sql — Integrated National Health Platform
-- MFA enrolment store (docs/08, docs/66 gap 8b). Apply after 0003.
-- Auth-scoped (keyed to Django's auth_user), so no tenant RLS.
BEGIN;

CREATE TABLE mfa_devices (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    secret      TEXT NOT NULL,                          -- base32 TOTP secret
    confirmed   BOOLEAN NOT NULL DEFAULT false,         -- true once the user proves a code
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;
