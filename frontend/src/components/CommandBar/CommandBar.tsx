import { useMemo, useState } from "react";
import { ACTIONS } from "../../lib/commands/registry";
import type { ActionSpec } from "../../lib/commands/types";
import { holdsCommand } from "../../lib/entitlements";

/** Entitlement-first command palette (docs/06): shows only the actions whose command the
 * caller holds, grouped by domain, filtered by a search box. Selecting one runs it. */
export function CommandBar({ onSelect }: { onSelect: (spec: ActionSpec) => void }) {
  const [query, setQuery] = useState("");

  const held = useMemo(() => ACTIONS.filter((a) => holdsCommand(a.command)), []);
  const groups = useMemo(() => {
    const q = query.trim().toLowerCase();
    const matched = held.filter((a) =>
      `${a.command} ${a.label} ${a.domain}`.toLowerCase().includes(q),
    );
    const byDomain = new Map<string, ActionSpec[]>();
    for (const a of matched) {
      if (!byDomain.has(a.domain)) byDomain.set(a.domain, []);
      byDomain.get(a.domain)!.push(a);
    }
    return [...byDomain.entries()];
  }, [held, query]);

  if (held.length === 0) {
    return (
      <p style={{ color: "var(--color-text-secondary)" }}>
        You don't hold any commands yet. Ask an administrator to assign a command bundle.
      </p>
    );
  }

  return (
    <div>
      <input
        aria-label="Type a command or search"
        placeholder="Type a command or search…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          width: "100%",
          maxWidth: 480,
          padding: 8,
          border: "1px solid var(--color-border-strong)",
          borderRadius: "var(--radius)",
        }}
      />
      {groups.length === 0 && <p>No commands match “{query}”.</p>}
      {groups.map(([domain, actions]) => (
        <div key={domain} style={{ marginTop: 16 }}>
          <h4 style={{ margin: "0 0 4px", color: "var(--color-brand-deep)" }}>{domain}</h4>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {actions.map((a) => (
              <button
                key={a.id}
                onClick={() => onSelect(a)}
                title={`${a.method} /api/v1${a.path}`}
                style={{
                  padding: "6px 10px",
                  border: "1px solid var(--color-border-strong)",
                  borderRadius: "var(--radius)",
                  background: "var(--color-surface)",
                  cursor: "pointer",
                }}
              >
                <kbd>{a.command}</kbd> {a.label}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
