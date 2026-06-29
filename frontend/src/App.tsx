import { CommandBar } from "./components/CommandBar/CommandBar";

/** Skeleton shell — one unified, command-driven surface (docs/06). */
export function App() {
  return (
    <main style={{ padding: "var(--space)" }}>
      <header style={{ background: "var(--color-brand-deep)", color: "#fff", padding: 12 }}>
        🏥 Integrated National Health Platform
      </header>
      <h2>Command bar</h2>
      <CommandBar />
    </main>
  );
}
