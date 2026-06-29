import { useAuthStore, type CommandCode } from "./auth/store";

/** Single source of truth for "can this user do X" — drives tiles, routes, and the command bar. */
export const holdsCommand = (code: CommandCode): boolean =>
  useAuthStore.getState().commands.has(code);
