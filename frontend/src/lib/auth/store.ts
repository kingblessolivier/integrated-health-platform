import { create } from "zustand";

export type CommandCode = string;

interface AuthState {
  token: string | null;
  userId: string | null;
  tenantId: string | null;
  commands: Set<CommandCode>;
  setSession: (s: { token: string; userId: string; tenantId: string; commands: CommandCode[] }) => void;
  forceLogout: (reason?: string) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  userId: null,
  tenantId: null,
  commands: new Set(),
  setSession: ({ token, userId, tenantId, commands }) =>
    set({ token, userId, tenantId, commands: new Set(commands) }),
  forceLogout: () => set({ token: null, userId: null, tenantId: null, commands: new Set() }),
}));
