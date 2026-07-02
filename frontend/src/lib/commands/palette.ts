import { domainOrder } from "./domains";
import type { ActionSpec } from "./types";

/** Pure ranking for the ⌘K palette: exact/prefix command-code matches first, then label/
 * domain substring matches, preserving registry order within a tier. Empty query = all. */
export function rankCommands(query: string, actions: ActionSpec[]): ActionSpec[] {
  const q = query.trim().toLowerCase();
  if (!q) return actions;
  const scored: { a: ActionSpec; score: number }[] = [];
  for (const a of actions) {
    const code = a.command.toLowerCase();
    const hay = `${a.label} ${a.domain}`.toLowerCase();
    let score = -1;
    if (code === q) score = 0;
    else if (code.startsWith(q)) score = 1;
    else if (code.includes(q)) score = 2;
    else if (hay.includes(q)) score = 3;
    if (score >= 0) scored.push({ a, score });
  }
  return scored
    .map((s, i) => ({ ...s, i })) // stable
    .sort((x, y) => x.score - y.score || x.i - y.i)
    .map((s) => s.a);
}

/** Group actions by domain, ordered per DOMAINS. */
export function groupByDomain(actions: ActionSpec[]): [string, ActionSpec[]][] {
  const map = new Map<string, ActionSpec[]>();
  for (const a of actions) {
    if (!map.has(a.domain)) map.set(a.domain, []);
    map.get(a.domain)!.push(a);
  }
  return [...map.entries()].sort((a, b) => domainOrder(a[0]) - domainOrder(b[0]));
}
