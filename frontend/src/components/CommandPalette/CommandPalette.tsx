import { useEffect, useMemo, useRef, useState } from "react";
import { actionById, ACTIONS } from "../../lib/commands/registry";
import { rankCommands } from "../../lib/commands/palette";
import type { ActionSpec } from "../../lib/commands/types";
import { holdsCommand } from "../../lib/entitlements";
import { useUiStore } from "../../lib/ui/store";

/** ⌘K entitlement-aware command palette (docs/06 §command-bar interaction): open with
 * ⌘K/Ctrl-K, type a code or label, arrow-navigate, Enter to run. Recents surface first when
 * the query is empty. Only commands the user holds are ever listed. */
export function CommandPalette({
  open,
  onClose,
  onRun,
}: {
  open: boolean;
  onClose: () => void;
  onRun: (spec: ActionSpec) => void;
}) {
  const recents = useUiStore((s) => s.recents);
  const [query, setQuery] = useState("");
  const [cursor, setCursor] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const held = useMemo(() => ACTIONS.filter((a) => holdsCommand(a.command)), []);
  const list = useMemo(() => {
    if (!query.trim()) {
      const recentActions = recents.map(actionById).filter(Boolean) as ActionSpec[];
      const recentHeld = recentActions.filter((a) => holdsCommand(a.command));
      const rest = held.filter((a) => !recents.includes(a.id));
      return [...recentHeld, ...rest];
    }
    return rankCommands(query, held);
  }, [query, held, recents]);

  useEffect(() => {
    if (open) {
      setQuery("");
      setCursor(0);
      // focus after paint
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [open]);
  useEffect(() => setCursor(0), [query]);

  if (!open) return null;

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Escape") return onClose();
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setCursor((c) => Math.min(c + 1, list.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setCursor((c) => Math.max(c - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const chosen = list[cursor];
      if (chosen) onRun(chosen);
    }
  }

  const showingRecents = !query.trim() && recents.length > 0;

  return (
    <div className="palette__backdrop" onMouseDown={onClose}>
      <div className="palette" role="dialog" aria-label="Command palette" onMouseDown={(e) => e.stopPropagation()}>
        <input
          ref={inputRef}
          className="palette__input"
          placeholder="Type a command or search…   (Esc to close)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={onKeyDown}
        />
        <div className="palette__list">
          {showingRecents && <div className="palette__section">Recent</div>}
          {list.length === 0 && <div className="palette__empty">No commands match “{query}”.</div>}
          {list.map((a, i) => (
            <button
              key={a.id}
              className={`palette__item${i === cursor ? " is-active" : ""}`}
              onMouseEnter={() => setCursor(i)}
              onClick={() => onRun(a)}
            >
              <span className="badge">{a.command}</span>
              <span className="palette__label">{a.label}</span>
              <span className="palette__domain">{a.domain}</span>
              <span className={`method method--${a.method}`}>{a.method}</span>
            </button>
          ))}
        </div>
        <div className="palette__foot">
          <span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
          <span><kbd>↵</kbd> run</span>
          <span><kbd>esc</kbd> close</span>
          <span className="spacer" />
          <span>{list.length} of {held.length} commands</span>
        </div>
      </div>
    </div>
  );
}
