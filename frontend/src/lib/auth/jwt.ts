/**
 * Decode the four-axis claims the backend mints (apps/accounts/tokens.py):
 *   user_id, tenant_id, geo_scope, max_sensitivity, commands[]
 *
 * This only READS the payload for UI gating — it does not verify the signature.
 * The server is the authority: every request is re-checked against the token, so a
 * tampered client payload buys nothing (it just gets 401/403 on the next call).
 */
export interface Claims {
  userId: string;
  tenantId: string;
  geoScope: unknown;
  maxSensitivity: string;
  commands: string[];
  exp?: number;
}

function base64UrlDecode(segment: string): string {
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/");
  const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
  return atob(padded + pad);
}

export function decodeClaims(token: string): Claims {
  const parts = token.split(".");
  if (parts.length !== 3) throw new Error("malformed token");
  const payload = JSON.parse(base64UrlDecode(parts[1])) as Record<string, unknown>;
  return {
    userId: String(payload.user_id ?? ""),
    tenantId: String(payload.tenant_id ?? ""),
    geoScope: payload.geo_scope ?? null,
    maxSensitivity: String(payload.max_sensitivity ?? "aggregate"),
    commands: Array.isArray(payload.commands) ? (payload.commands as string[]) : [],
    exp: typeof payload.exp === "number" ? payload.exp : undefined,
  };
}

/** True if the token is absent or past its `exp` (with a small skew allowance). */
export function isExpired(claims: Claims, nowSeconds: number = Date.now() / 1000): boolean {
  return claims.exp !== undefined && claims.exp <= nowSeconds - 5;
}
