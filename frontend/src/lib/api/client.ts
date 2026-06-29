import { useAuthStore } from "../auth/store";

const BASE = "/api/v1";

/** Thin fetch wrapper: attaches JWT + correlation id, normalises errors, handles 401/403. */
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const { token, forceLogout } = useAuthStore.getState();
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "X-Correlation-Id": crypto.randomUUID(),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init.headers,
    },
  });

  if (res.status === 401) {
    forceLogout("expired");
    throw new Error("unauthenticated");
  }
  if (res.status === 403) {
    // Out of scope — the server already terminated the session.
    forceLogout("scope_violation");
    throw new Error("forbidden");
  }
  if (!res.ok) throw await res.json().catch(() => new Error(`HTTP ${res.status}`));
  return res.json() as Promise<T>;
}
