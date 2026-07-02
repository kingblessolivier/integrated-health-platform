import { useEffect, useState } from "react";

/** Load-bearing sync state (docs/06): 🟢 Synced / 🟠 Offline, always visible. Status is shown
 * by icon + text, never colour alone (docs/05 accessibility). */
export function SyncPill() {
  const [online, setOnline] = useState(() =>
    typeof navigator === "undefined" ? true : navigator.onLine,
  );

  useEffect(() => {
    const up = () => setOnline(true);
    const down = () => setOnline(false);
    window.addEventListener("online", up);
    window.addEventListener("offline", down);
    return () => {
      window.removeEventListener("online", up);
      window.removeEventListener("offline", down);
    };
  }, []);

  return (
    <span className={`pill ${online ? "pill--ok" : "pill--warn"}`}>
      <span aria-hidden>{online ? "🟢" : "🟠"}</span>
      {online ? "Synced" : "Offline"}
    </span>
  );
}
