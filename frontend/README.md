# Frontend — Integrated National Health Platform (Web)

React 18 + TypeScript + Vite skeleton for the single command-driven dashboard
(docs [06](../docs/06-unified-dashboard.md), [50](../docs/50-frontend-architecture.md)).

## Layout
```
src/
  App.tsx                     shell
  components/CommandBar/      entitlement-filtered ⌘K palette
  lib/auth/store.ts           Zustand session (token, commands, scope)
  lib/entitlements.ts         holdsCommand() — single source of truth
  lib/api/client.ts           fetch wrapper (JWT, 401/403 handling)
  theme/tokens.css            design tokens (docs/05, corrected amber)
```

## Run
```bash
npm install
npm run dev      # proxies /api to http://localhost:8000
```

State: TanStack Query (server state) + Zustand (session). The UI renders only the commands
the user holds — tiles, routes, and the command bar all read the same `commands` set.
