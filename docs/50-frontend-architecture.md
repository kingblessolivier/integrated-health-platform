# 50 — Frontend Architecture (Web)

The React 18 + TypeScript SPA that renders the **single command-driven dashboard**
(doc 06). The UI is generated from the commands the user holds — there is no per-role
hand-built screen.

## Principles

- **Entitlement-first:** the app fetches the user's command bundle at login; every surface
  (tile launcher, command bar, routes) is filtered by it.
- **One dashboard:** routes are commands, not roles. Holding `RXDP` reveals the dispense
  surface; not holding it means the route, tile, and command-bar entry simply do not exist.
- **Tokens, not hex:** all colour/spacing comes from the shared design tokens (doc 05) as CSS
  variables, so web and Flutter stay in lockstep.

## Folder structure

```
src/
├── app/
│   ├── routes.tsx              # command-keyed routes, lazy-loaded
│   └── providers.tsx          # query client, auth, theme
├── features/                   # one folder per command domain (PT, RX, EN, LB, …)
│   ├── patient/                # PTRG, PTSR, PTVW … components + hooks
│   ├── prescription/           # RXNW, RXVF, RXDP …
│   └── analytics/              # ANVW dashboard widgets
├── components/
│   ├── CommandBar/             # ⌘K palette, entitlement-filtered
│   ├── TileLauncher/           # dynamic grid from held commands
│   ├── SyncBanner/             # synced/offline/error states (doc 05)
│   ├── StatusBadge/  KpiCard/  DrillDownMap/  FefoBatchPicker/
│   └── NidaLookupField/  ConsentToggle/  BarcodeScanOverlay/
├── lib/
│   ├── api/                    # generated client from the OpenAPI spec (doc 49)
│   ├── auth/                   # JWT handling, refresh, 403 → lock flow
│   └── entitlements.ts         # holdsCommand(code) helper
├── store/                      # global state (see below)
└── theme/
    ├── tokens.css              # design tokens as CSS variables
    └── theme.ts                # typed token accessors
```

## State management

- **Server state:** **TanStack Query** (caching, retries, optimistic updates, background
  refetch) — most screens are server-driven.
- **Client/session state:** **Zustand** — small, typed stores for `auth` (user, commands,
  scope), `command` (active command context), and `ui` (density, banners). Redux Toolkit is
  an acceptable alternative if the team prefers a single store + devtools.
- **Why not all-Redux:** the data is overwhelmingly server state; Query + a thin Zustand
  layer keeps boilerplate low and the entitlement logic explicit.

## Command-bar entitlement filtering

```ts
// lib/entitlements.ts
export const holdsCommand = (code: CommandCode) =>
  useAuthStore.getState().commands.has(code);

// components/CommandBar/useCommandPalette.ts
const palette = ALL_COMMANDS
  .filter(c => holdsCommand(c.code))      // never show what the user cannot do
  .filter(c => matches(query, c));         // ⌘K fuzzy search
```

Tiles, routes, and the palette all read the **same** `commands` set, so there is one source
of truth for "what can this user do".

## API client & 403 handling

```ts
// lib/api/interceptor.ts
client.interceptors.response.use(undefined, (err) => {
  if (err.status === 401) return auth.refreshThenRetry(err);
  if (err.status === 403) {            // out of scope → server already locked the session
    auth.forceLogout('scope_violation');
  }
  return Promise.reject(normaliseError(err)); // → standard error envelope (doc 49)
});
```

Every mutating call attaches an `Idempotency-Key` and `X-Correlation-Id`.

## Accessibility & density

- Two density modes (dense clinical / spacious CHW-patient) driven by a token set (doc 05).
- WCAG 2.2 AA enforced in CI via `axe-core` checks on key screens; colour-contrast lint on
  the token file so a failing pair (e.g. white-on-amber) never ships.
- Status is never colour-alone: `StatusBadge` always renders icon + text.

## Build & quality

- Vite build; code-split per feature/command.
- Type-safe API client generated from the OpenAPI spec (doc 49) — contract drift fails CI.
- Unit (Vitest) + component (Testing Library) + E2E (Playwright) per
  [29 — Testing Strategy](29-testing-strategy-and-qa.md).
