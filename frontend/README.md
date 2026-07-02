# Frontend — Integrated National Health Platform (Web)

React 18 + TypeScript + Vite skeleton for the single command-driven dashboard
(docs [06](../docs/06-unified-dashboard.md), [50](../docs/50-frontend-architecture.md)).

## Layout
```
src/
  App.tsx                     auth-gated shell (login → command-driven surface)
  components/CommandBar/      entitlement-filtered ⌘K palette
  components/ui/Field.tsx     labelled input on the design tokens
  features/login/             sign-in (four-axis JWT; OTP step when MFA is on)
  features/patients/          patient search (PTSR) + register (PTRG) — first API slice
  features/mfa/               self-service MFA enrolment (enrol → confirm)
  lib/auth/store.ts           Zustand session (token, commands, scope) + localStorage
  lib/auth/jwt.ts             decode four-axis claims from the JWT (UI gating only)
  lib/entitlements.ts         holdsCommand() — single source of truth
  lib/api/client.ts           fetch wrapper (JWT, 401/403 handling)
  lib/api/auth.ts             login + MFA enrol/confirm
  lib/api/patients.ts         patient search / register
  theme/tokens.css            design tokens (docs/05, corrected amber)
```

## Run
```bash
npm install
npm run dev      # proxies /api to http://localhost:8000
npm test         # vitest (jwt decode + auth store)
npm run build    # tsc (strict) + vite build
```

State: TanStack Query (server state) + Zustand (session). The UI renders only the commands
the user holds — the command bar and each screen read the same `commands` set, decoded from
the JWT at login. The server re-checks every request, so client-side gating is UX only.

## First vertical slice (this drop)
Login → four-axis JWT → command-gated Patients screen, plus MFA enrolment. This is the
end-to-end path (auth → command gate → audit) rendered in the browser; it exercises the
backend contract from `docs/49`.
