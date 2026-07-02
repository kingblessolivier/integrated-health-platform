import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api/client";
import { actionById } from "../../lib/commands/registry";
import type { ActionSpec } from "../../lib/commands/types";
import { holdsCommand } from "../../lib/entitlements";
import { useUiStore } from "../../lib/ui/store";

/** ANVW — the dashboard held by every user, rendered at their data altitude (docs/06).
 * KPI widgets fetch the real analytics endpoints the user holds; values show "—" until the
 * backend is reachable (no fabricated data). Recents give quick re-entry. */
export function Dashboard({ onOpen }: { onOpen: (spec: ActionSpec) => void }) {
  const recents = useUiStore((s) => s.recents);
  const recentActions = recents.map(actionById).filter(Boolean) as ActionSpec[];

  return (
    <div>
      <div className="kpi-row">
        <Kpi command="SVAL" title="Open outbreak alerts" path="/surveillance/alerts/"
          derive={(d) => arr(d, "alerts").length} />
        <Kpi command="STEX" title="Batches expiring ≤30d" path="/stock/expiring/"
          derive={(d) => bucket(d, "expired") + bucket(d, "30")} />
        <Kpi command="SVMP" title="Disease clusters" path="/surveillance/clusters/"
          derive={(d) => Object.keys(obj(d, "counts")).length} />
        <Kpi command="HRLC" title="Licences tracked" path="/hr/licences/"
          derive={(d) => arr(d, "licences").length} />
        <Kpi command="CBFB" title="CBHI fund balance" path="/cbhi/fund/"
          derive={(d) => money(d)} />
      </div>

      {recentActions.length > 0 && (
        <section className="card" style={{ marginTop: "var(--s-5)" }}>
          <h3 className="card__title">Recent commands</h3>
          <div className="tile-grid">
            {recentActions.map((a) => (
              <button key={a.id} className="tile" onClick={() => onOpen(a)}>
                <span className="tile__label">{a.label}</span>
                <span className="badge">{a.command}</span>
              </button>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function Kpi({
  command,
  title,
  path,
  derive,
}: {
  command: string;
  title: string;
  path: string;
  derive: (data: unknown) => number | string;
}) {
  const held = holdsCommand(command);
  const q = useQuery({
    queryKey: ["kpi", command],
    queryFn: () => api(path),
    enabled: held,
    retry: false,
    staleTime: 30_000,
  });

  if (!held) return null;

  let value: string = "—";
  let sub = "Awaiting connection";
  if (q.isLoading) sub = "Loading…";
  else if (q.isError) sub = "Backend unreachable";
  else if (q.data !== undefined) {
    value = String(derive(q.data));
    sub = "Live";
  }

  return (
    <div className="kpi">
      <div className="kpi__value">{value}</div>
      <div className="kpi__title">{title}</div>
      <div className="kpi__sub">
        <span className="badge">{command}</span> {sub}
      </div>
    </div>
  );
}

// Defensive extractors for varied endpoint shapes.
const obj = (d: unknown, k: string): Record<string, unknown> => {
  const v = (d as Record<string, unknown>)?.[k];
  return v && typeof v === "object" ? (v as Record<string, unknown>) : {};
};
const arr = (d: unknown, k: string): unknown[] => {
  const v = (d as Record<string, unknown>)?.[k];
  return Array.isArray(v) ? v : [];
};
const bucket = (d: unknown, k: string): number => arr(obj(d, "buckets") as unknown, k).length;
function money(d: unknown): string {
  const o = d as Record<string, unknown>;
  const bal = Number(o?.balance ?? Number(o?.premiums ?? 0) - Number(o?.claims_paid ?? 0));
  return Number.isFinite(bal) ? bal.toLocaleString() : "—";
}
