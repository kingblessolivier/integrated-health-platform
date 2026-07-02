import { useMemo } from "react";
import { domainIcon } from "../../lib/commands/domains";
import { groupByDomain } from "../../lib/commands/palette";
import { ACTIONS } from "../../lib/commands/registry";
import type { ActionSpec } from "../../lib/commands/types";
import { holdsCommand } from "../../lib/entitlements";

/** Auto-generated grid of the user's entitled commands (docs/06 mode 2) — for occasional /
 * lower-literacy staff. Icon + label, grouped by domain. */
export function TileLauncher({
  onSelect,
  only,
}: {
  onSelect: (spec: ActionSpec) => void;
  only?: string;
}) {
  const groups = useMemo(
    () =>
      groupByDomain(
        ACTIONS.filter((a) => holdsCommand(a.command) && (!only || a.domain === only)),
      ),
    [only],
  );

  if (groups.length === 0) {
    return (
      <div className="empty">
        <div className="empty__icon">🔑</div>
        <div className="empty__title">No commands assigned yet</div>
        <div className="empty__hint">Ask an administrator to assign you a command bundle.</div>
      </div>
    );
  }

  return (
    <div>
      {groups.map(([domain, actions]) => (
        <section key={domain} className="tile-group">
          <h3 className="tile-group__title">
            <span aria-hidden>{domainIcon(domain)}</span> {domain}
          </h3>
          <div className="tile-grid">
            {actions.map((a) => (
              <button key={a.id} className="tile" onClick={() => onSelect(a)}>
                <span className="tile__icon" aria-hidden>{domainIcon(domain)}</span>
                <span className="tile__label">{a.label}</span>
                <span className="badge">{a.command}</span>
              </button>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
