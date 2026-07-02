import { create } from "zustand";
import { decodeClaims } from "./jwt";

export type CommandCode = string;
export type LogoutReason = "expired" | "scope_violation" | "user" | null;

const TOKEN_KEY = "inhp.token";

interface AuthState {
  token: string | null;
  userId: string | null;
  tenantId: string | null;
  maxSensitivity: string;
  commands: Set<CommandCode>;
  logoutReason: LogoutReason;
  /** Establish a session from a raw access token (decodes the four-axis claims). */
  setToken: (token: string) => void;
  forceLogout: (reason?: LogoutReason) => void;
}

function readStoredToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

function persist(token: string | null) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* storage unavailable (private mode) — session stays in-memory */
  }
}

const LOGGED_OUT = {
  userId: null,
  tenantId: null,
  maxSensitivity: "aggregate",
  commands: new Set<CommandCode>(),
};

function claimsFor(token: string) {
  const c = decodeClaims(token);
  return {
    userId: c.userId,
    tenantId: c.tenantId,
    maxSensitivity: c.maxSensitivity,
    commands: new Set(c.commands),
  };
}

/** A persisted token could be corrupt; fall back to logged-out rather than throwing at boot. */
function bootSession(token: string | null) {
  if (!token) return { token: null, ...LOGGED_OUT };
  try {
    return { token, ...claimsFor(token) };
  } catch {
    persist(null);
    return { token: null, ...LOGGED_OUT };
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  ...bootSession(readStoredToken()),
  logoutReason: null,
  setToken: (token) => {
    persist(token);
    set({ token, logoutReason: null, ...claimsFor(token) });
  },
  forceLogout: (reason = "user") => {
    persist(null);
    set({ token: null, ...LOGGED_OUT, logoutReason: reason });
  },
}));
