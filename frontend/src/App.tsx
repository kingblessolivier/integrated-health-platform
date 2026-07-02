import { useState } from "react";
import { CommandBar } from "./components/CommandBar/CommandBar";
import { ActionRunner } from "./features/command/ActionRunner";
import { LoginScreen } from "./features/login/LoginScreen";
import { MfaScreen } from "./features/mfa/MfaScreen";
import { PatientsScreen } from "./features/patients/PatientsScreen";
import { useAuthStore } from "./lib/auth/store";
import type { ActionSpec } from "./lib/commands/types";

type View = "home" | "patients" | "mfa";

const NAV: { key: View; label: string; icon: string }[] = [
  { key: "home", label: "Commands", icon: "⌘" },
  { key: "patients", label: "Patients", icon: "👤" },
  { key: "mfa", label: "Security", icon: "🔐" },
];

const HEADINGS: Record<View, { title: string; sub: string }> = {
  home: { title: "Command centre", sub: "Run any action you're entitled to." },
  patients: { title: "Patients", sub: "Search the master index or register a new patient." },
  mfa: { title: "Two-factor authentication", sub: "Protect your account with an authenticator app." },
};

/** One unified, command-driven surface (docs/06). Auth-gated: no token → login. */
export function App() {
  const token = useAuthStore((s) => s.token);
  const userId = useAuthStore((s) => s.userId);
  const commandCount = useAuthStore((s) => s.commands.size);
  const forceLogout = useAuthStore((s) => s.forceLogout);
  const [view, setView] = useState<View>("home");
  const [action, setAction] = useState<ActionSpec | null>(null);

  if (!token) return <LoginScreen />;

  const heading = HEADINGS[view];
  const initials = (userId ?? "?").slice(0, 2).toUpperCase();

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="sidebar__brand">
          <span className="sidebar__brand-mark">🏥</span>
          <span>Integrated National Health Platform</span>
        </div>
        <nav className="nav">
          <div className="nav__section">Workspace</div>
          {NAV.map((n) => (
            <button
              key={n.key}
              className="nav__item"
              aria-current={view === n.key}
              onClick={() => {
                setView(n.key);
                setAction(null);
              }}
            >
              <span className="nav__item-icon">{n.icon}</span>
              {n.label}
            </button>
          ))}
        </nav>
        <div className="sidebar__foot">{commandCount} command{commandCount === 1 ? "" : "s"} held</div>
      </aside>

      <div>
        <header className="topbar">
          <div className="topbar__title">{heading.title}</div>
          <div className="user-chip">
            <div className="user-chip__meta">
              <span className="user-chip__id">{userId}</span>
              <span className="user-chip__sub">{commandCount} commands</span>
            </div>
            <div className="avatar" aria-hidden>{initials}</div>
            <button className="btn btn--ghost btn--sm" onClick={() => forceLogout("user")}>
              Sign out
            </button>
          </div>
        </header>

        <main className="content">
          <div className="content__head">
            <h2>{heading.title}</h2>
            <p>{heading.sub}</p>
          </div>

          {view === "home" && (
            <div className="grid-2">
              <div className="card">
                <CommandBar onSelect={setAction} activeId={action?.id} />
              </div>
              {action ? (
                <ActionRunner spec={action} />
              ) : (
                <div className="card">
                  <div className="empty">
                    <div className="empty__icon">⌘</div>
                    <div className="empty__title">Pick a command to begin</div>
                    <div className="empty__hint">
                      Choose an action on the left. Only the commands you're entitled to are shown —
                      the server re-checks every request.
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
          {view === "patients" && <PatientsScreen />}
          {view === "mfa" && <MfaScreen />}
        </main>
      </div>
    </div>
  );
}
