import { create } from "zustand";

export type Density = "comfortable" | "compact";

const DENSITY_KEY = "inhp.density";
const RECENTS_KEY = "inhp.recents";
const MAX_RECENTS = 6;

function read<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key);
    return v ? (JSON.parse(v) as T) : fallback;
  } catch {
    return fallback;
  }
}
function write(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* ignore */
  }
}

interface UiState {
  density: Density;
  recents: string[]; // action ids, most-recent first
  setDensity: (d: Density) => void;
  toggleDensity: () => void;
  pushRecent: (id: string) => void;
}

export const useUiStore = create<UiState>((set, get) => ({
  density: read<Density>(DENSITY_KEY, "comfortable"),
  recents: read<string[]>(RECENTS_KEY, []),
  setDensity: (density) => {
    write(DENSITY_KEY, density);
    set({ density });
  },
  toggleDensity: () => get().setDensity(get().density === "compact" ? "comfortable" : "compact"),
  pushRecent: (id) => {
    const recents = [id, ...get().recents.filter((r) => r !== id)].slice(0, MAX_RECENTS);
    write(RECENTS_KEY, recents);
    set({ recents });
  },
}));
