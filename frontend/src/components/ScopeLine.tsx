import { useAuthStore } from "../lib/auth/store";

const SENSITIVITY_LABEL: Record<string, string> = {
  individual: "Individual records",
  facility: "Facility-level",
  aggregate: "Aggregate only",
};

function geoSummary(geo: unknown): string {
  if (!geo || typeof geo !== "object") return "National";
  const g = geo as Record<string, unknown>;
  const parts = ["village", "cell", "sector", "district", "province"]
    .map((k) => g[k])
    .filter(Boolean)
    .map(String);
  return parts.length ? parts.join(" · ") : "National";
}

/** Persistent "Your scope" line — the four-axis window the user is in (docs/06 rule:
 * "Scope is visible"). Reassures the user which data altitude they're operating at. */
export function ScopeLine() {
  const tenantId = useAuthStore((s) => s.tenantId);
  const maxSensitivity = useAuthStore((s) => s.maxSensitivity);
  const geoScope = useAuthStore((s) => s.geoScope);

  return (
    <div className="scopeline" role="note" aria-label="Your data scope">
      <span className="scopeline__label">Your scope</span>
      <span className="scopeline__item">🔎 {SENSITIVITY_LABEL[maxSensitivity] ?? maxSensitivity}</span>
      <span className="scopeline__sep">·</span>
      <span className="scopeline__item">🏢 Tenant {tenantId ? shorten(tenantId) : "—"}</span>
      <span className="scopeline__sep">·</span>
      <span className="scopeline__item">📍 {geoSummary(geoScope)}</span>
    </div>
  );
}

const shorten = (id: string) => (id.length > 10 ? `${id.slice(0, 8)}…` : id);
