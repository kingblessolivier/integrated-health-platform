import { useMemo, useState } from "react";
import { holdsCommand } from "../../lib/entitlements";

/** Illustrative slice of the catalogue (docs/03). Load the full set from the API in real use. */
const ALL_COMMANDS = [
  { code: "PTRG", label: "Register patient" },
  { code: "PTSR", label: "Search patient" },
  { code: "ENNW", label: "Open encounter" },
  { code: "ENDX", label: "Diagnose (ICD)" },
  { code: "RXNW", label: "Prescribe" },
  { code: "RXDP", label: "Dispense (FEFO)" },
  { code: "ANVW", label: "Dashboard" },
];

export function CommandBar() {
  const [query, setQuery] = useState("");
  // Only commands the user holds are ever shown — entitlement-first.
  const visible = useMemo(
    () =>
      ALL_COMMANDS.filter((c) => holdsCommand(c.code)).filter((c) =>
        `${c.code} ${c.label}`.toLowerCase().includes(query.toLowerCase()),
      ),
    [query],
  );

  return (
    <div>
      <input
        aria-label="Type a command or search"
        placeholder="Type a command or search…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <ul>
        {visible.map((c) => (
          <li key={c.code}>
            <kbd>{c.code}</kbd> {c.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
