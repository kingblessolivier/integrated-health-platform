/**
 * Auth calls. Login deliberately bypasses the shared `api()` wrapper: a 401 during login
 * means "bad credentials" or "MFA required", not "session expired", so we must read the
 * body instead of triggering the global force-logout.
 */
import { api } from "./client";

const BASE = "/api/v1";

export interface LoginResult {
  access: string;
  refresh: string;
}

export class MfaRequiredError extends Error {
  constructor() {
    super("mfa_required");
    this.name = "MfaRequiredError";
  }
}

export class LoginError extends Error {}

export async function login(nidaId: string, password: string, otp?: string): Promise<LoginResult> {
  const body: Record<string, string> = { username: nidaId, password };
  if (otp) body.otp = otp;
  const res = await fetch(`${BASE}/auth/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Correlation-Id": crypto.randomUUID() },
    body: JSON.stringify(body),
  });
  if (res.status === 401) {
    const data = await res.json().catch(() => ({}));
    if (data?.code === "mfa_required" || data?.detail === "mfa_required") {
      throw new MfaRequiredError();
    }
    throw new LoginError("Invalid national ID or password.");
  }
  if (!res.ok) throw new LoginError(`Login failed (HTTP ${res.status}).`);
  return (await res.json()) as LoginResult;
}

export interface EnrolResult {
  secret: string;
  otpauth_uri: string;
}

/** Tier-2 (authenticated, no command) — uses the shared wrapper so the JWT is attached. */
export const mfaEnrol = () => api<EnrolResult>("/auth/mfa/enrol/", { method: "POST", body: "{}" });

export const mfaConfirm = (otp: string) =>
  api<{ status: string }>("/auth/mfa/confirm/", {
    method: "POST",
    body: JSON.stringify({ otp }),
  });
