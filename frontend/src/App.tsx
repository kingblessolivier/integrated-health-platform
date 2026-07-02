import { useEffect, useMemo, useState } from "react";
import { CommandPalette } from "./components/CommandPalette/CommandPalette";
import { ScopeLine } from "./components/ScopeLine";
import { SyncPill } from "./components/SyncPill";
import { TileLauncher } from "./components/TileLauncher/TileLauncher";
import { ActionRunner } from "./features/command/ActionRunner";
import { Dashboard } from "./features/dashboard/Dashboard";
import { LoginScreen } from "./features/login/LoginScreen";
import { MfaScreen } from "./features/mfa/MfaScreen";
import { PatientsScreen } from "./features/patients/PatientsScreen";
import { useAuthStore } from "./lib/auth/store";
import { domainIcon } from "./lib/commands/domains";
import { groupByDomain } from "./lib/commands/palette";
import { ACTIONS } from "./lib/commands/registry";
import type { ActionSpec } from "./lib/commands/types";
import { holdsCommand } from "./lib/entitlements";
import { useUiStore } from "./lib/ui/store";

type View =
  | { kind: "dashboard" }
  | { kind: "tiles"; domain?: string }
  | { kind: "command"; spec: ActionSpec }
  | { kind: "patients" }
  | { kind: "mfa" };

const HEAD: Record<string, { title: string; sub: string }> = {
  dashboard: { title: "Dashboard", sub: "Your view, at your data altitude (ANVW)." },
  tiles: { title: "Commands", sub: "Everything you're entitled to do." },
  command: { title: "Run command", sub: "Fill in the details and execute." },
  patients: { title: "Patients", sub: "Search the master index or register a new patient." },
  mfa: { title: "Security", sub: "Protect your account with two-factor authentication." },
};

export function App() {
  const token = useAuthStore((s) => s.token);
  const userId = useAuthStore((s) => s.userId);
  const commandCount = useAuthStore((s) => s.commands.size);
  const forceLogout = useAuthStore((s) => s.forceLogout);
  const density = useUiStore((s) => s.density);
  const toggleDensity = useUiStore((s) => s.toggleDensity);
  const pushRecent = useUiStore((s) => s.pushRecent);

  const [view, setView] = useState<View>({ kind: "dashboard" });
  const [paletteOpen, setPaletteOpen] = useState(false);

  // ⌘K / Ctrl-K opens the palette anywhere (docs/06).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const heldDomains = useMemo(
    () => groupByDomain(ACTIONS.filter((a) => holdsCommand(a.command))).map(([d, a]) => ({ d, n: a.length })),
    // recompute per login (commandCount changes)
    [commandCount],
  );

  if (!token) return <LoginScreen />;

  function run(spec: ActionSpec) {
    pushRecent(spec.id);
    setView({ kind: "command", spec });
    setPaletteOpen(false);
  }

  const head = HEAD[view.kind];
  const initials = (userId ?? "?").slice(0, 2).toUpperCase();

  return (
    <div className={`shell ${density === "compact" ? "is-compact" : ""}`}>
      <aside className="sidebar">
        <div className="sidebar__brand">
          <span className="sidebar__brand-mark">🏥</span>
          <span>Integrated National Health Platform</span>
        </div>
        <nav className="nav">
          <div className="nav__section">Workspace</div>
          <NavItem active={view.kind === "dashboard"} icon="📊" label="Dashboard"
            onClick={() => setView({ kind: "dashboard" })} />
          <button className="nav__item" onClick={() => setPaletteOpen(true)}>
            <span className="nav__item-icon">⌘</span> Command palette
            <span className="kbd-hint">⌘K</span>
          </button>
          <NavItem active={view.kind === "tiles" && !view.domain} icon="▦" label="All commands"
            onClick={() => setView({ kind: "tiles" })} />
          <NavItem active={view.kind === "patients"} icon="👤" label="Patients"
            onClick={() => setView({ kind: "patients" })} />
          <NavItem active={view.kind === "mfa"} icon="🔐" label="Security"
            onClick={() => setView({ kind: "mfa" })} />

          {heldDomains.length > 0 && <div className="nav__section">Domains</div>}
          {heldDomains.map(({ d, n }) => (
            <button
              key={d}
              className="nav__item"
              aria-current={view.kind === "tiles" && view.domain === d}
              onClick={() => setView({ kind: "tiles", domain: d })}
            >
              <span className="nav__item-icon">{domainIcon(d)}</span>
              {d}
              <span className="nav__count">{n}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar__foot">{commandCount} command{commandCount === 1 ? "" : "s"} held</div>
      </aside>

      <div>
        <header className="topbar">
          <button className="cmd-trigger" onClick={() => setPaletteOpen(true)}>
            <span aria-hidden>🔍</span> Type a command or search…
            <span className="kbd-hint">⌘K</span>
          </button>
          <div className="topbar__right">
            <SyncPill />
            <button className="btn btn--ghost btn--sm" onClick={toggleDensity} title="Toggle density">
              {density === "compact" ? "Comfortable" : "Compact"}
            </button>
            <div className="user-chip">
              <div className="user-chip__meta">
                <span className="user-chip__id">{userId}</span>
                <span className="user-chip__sub">{commandCount} commands</span>
              </div>
              <div className="avatar" aria-hidden>{initials}</div>
            </div>
            <button className="btn btn--ghost btn--sm" onClick={() => forceLogout("user")}>Sign out</button>
          </div>
        </header>

        <ScopeLine />

        <main className="content">
          <div className="content__head">
            <h2>{view.kind === "command" ? view.spec.label : head.title}</h2>
            <p>{view.kind === "command" ? `${view.spec.domain} · ${view.spec.command}` : head.sub}</p>
          </div>

          {view.kind === "dashboard" && <Dashboard onOpen={run} />}
          {view.kind === "tiles" && <TileLauncher onSelect={run} only={view.domain} />}
          {view.kind === "command" && (
            <div className="grid-2">
              <ActionRunner spec={view.spec} />
              <div className="card">
                <h3 className="card__title">About this command</h3>
                <p className="card__subtitle">
                  <span className="badge">{view.spec.command}</span> {view.spec.label}
                </p>
                <table className="kv">
                  <tbody>
                    <tr><td>Domain</td><td>{view.spec.domain}</td></tr>
                    <tr><td>Method</td><td><span className={`method method--${view.spec.method}`}>{view.spec.method}</span></td></tr>
                    <tr><td>Endpoint</td><td><code>/api/v1{view.spec.path}</code></td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {view.kind === "patients" && <PatientsScreen />}
          {view.kind === "mfa" && <MfaScreen />}
        </main>
      </div>

      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} onRun={run} />
    </div>
  );
}

function NavItem({
  active,
  icon,
  label,
  onClick,
}: {
  active: boolean;
  icon: string;
  label: string;
  onClick: () => void;
}) {
  return (
    <button className="nav__item" aria-current={active} onClick={onClick}>
      <span className="nav__item-icon">{icon}</span>
      {label}
    </button>
  );
}
