import { useMemo, useState } from "react";
import { ACTIONS } from "../../lib/commands/registry";
import type { ActionSpec } from "../../lib/commands/types";
import { holdsCommand } from "../../lib/entitlements";

/** Entitlement-first command palette (docs/06): shows only the actions whose command the
 * caller holds, grouped by domain, filtered by a search box. Selecting one runs it. */
export function CommandBar({
  onSelect,
  activeId,
}: {
  onSelect: (spec: ActionSpec) => void;
  activeId?: string;
}) {
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
      <div className="empty">
        <div className="empty__icon">🔑</div>
        <div className="empty__title">No commands assigned yet</div>
        <div className="empty__hint">
          Ask an administrator to assign you a command bundle. Once granted, your actions appear
          here automatically.
        </div>
      </div>
    );
  }

  return (
    <div>
      <input
        className="search"
        aria-label="Type a command or search"
        placeholder="Search commands…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {groups.length === 0 && (
        <p style={{ color: "var(--color-text-secondary)", marginTop: "var(--s-4)" }}>
          No commands match “{query}”.
        </p>
      )}
      {groups.map(([domain, actions]) => (
        <div key={domain} className="cmd-group">
          <div className="cmd-group__title">{domain}</div>
          <div className="cmd-tiles">
            {actions.map((a) => (
              <button
                key={a.id}
                className="cmd-tile"
                aria-pressed={activeId === a.id}
                onClick={() => onSelect(a)}
                title={`${a.method} /api/v1${a.path}`}
              >
                <span className="badge">{a.command}</span>
                <span className="cmd-tile__label">{a.label}</span>
                <span className={`method method--${a.method} cmd-tile__method`}>{a.method}</span>
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
