import { useState } from "react";
import { CommandBar } from "./components/CommandBar/CommandBar";
import { ActionRunner } from "./features/command/ActionRunner";
import { LoginScreen } from "./features/login/LoginScreen";
import { MfaScreen } from "./features/mfa/MfaScreen";
import { PatientsScreen } from "./features/patients/PatientsScreen";
import { useAuthStore } from "./lib/auth/store";
import type { ActionSpec } from "./lib/commands/types";

type View = "home" | "patients" | "mfa";

/** One unified, command-driven surface (docs/06). Auth-gated: no token → login. */
export function App() {
  const token = useAuthStore((s) => s.token);
  const userId = useAuthStore((s) => s.userId);
  const forceLogout = useAuthStore((s) => s.forceLogout);
  const [view, setView] = useState<View>("home");
  const [action, setAction] = useState<ActionSpec | null>(null);

  if (!token) return <LoginScreen />;

  return (
    <main style={{ padding: "var(--space)" }}>
      <header
        style={{
          background: "var(--color-brand-deep)",
          color: "#fff",
          padding: 12,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span>🏥 Integrated National Health Platform</span>
        <span style={{ fontSize: 13 }}>
          <span style={{ opacity: 0.8 }}>{userId}</span>{" "}
          <button
            onClick={() => forceLogout("user")}
            style={{ marginLeft: 8, cursor: "pointer" }}
          >
            Sign out
          </button>
        </span>
      </header>

      <nav style={{ display: "flex", gap: 8, margin: "var(--space) 0" }}>
        <button onClick={() => setView("home")} aria-current={view === "home"}>
          Commands
        </button>
        <button onClick={() => setView("patients")} aria-current={view === "patients"}>
          Patients
        </button>
        <button onClick={() => setView("mfa")} aria-current={view === "mfa"}>
          Security (MFA)
        </button>
      </nav>

      {view === "home" && (
        <div style={{ display: "grid", gap: 24, gridTemplateColumns: "minmax(280px, 1fr) 1fr", alignItems: "start" }}>
          <CommandBar onSelect={setAction} />
          {action ? (
            <ActionRunner spec={action} />
          ) : (
            <p style={{ color: "var(--color-text-secondary)" }}>
              Pick a command to run it. Only the commands you hold are shown.
            </p>
          )}
        </div>
      )}
      {view === "patients" && <PatientsScreen />}
      {view === "mfa" && <MfaScreen />}
    </main>
  );
}
