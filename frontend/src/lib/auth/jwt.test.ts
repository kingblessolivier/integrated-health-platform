import { describe, expect, it } from "vitest";
import { decodeClaims, isExpired } from "./jwt";

/** Build an unsigned JWT-shaped string (header.payload.signature) for decode tests. */
function makeToken(payload: Record<string, unknown>): string {
  const b64 = (o: unknown) =>
    btoa(JSON.stringify(o)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  return `${b64({ alg: "HS256", typ: "JWT" })}.${b64(payload)}.sig`;
}

describe("decodeClaims", () => {
  it("maps the four-axis claims", () => {
    const token = makeToken({
      user_id: "u-1",
      tenant_id: "t-1",
      geo_scope: { province: "Kigali" },
      max_sensitivity: "individual",
      commands: ["PTSR", "PTRG"],
      exp: 1893456000,
    });
    const c = decodeClaims(token);
    expect(c.userId).toBe("u-1");
    expect(c.tenantId).toBe("t-1");
    expect(c.maxSensitivity).toBe("individual");
    expect(c.commands).toEqual(["PTSR", "PTRG"]);
    expect(c.exp).toBe(1893456000);
  });

  it("defaults missing fields safely", () => {
    const c = decodeClaims(makeToken({ user_id: "u-2" }));
    expect(c.commands).toEqual([]);
    expect(c.maxSensitivity).toBe("aggregate");
    expect(c.tenantId).toBe("");
  });

  it("rejects a malformed token", () => {
    expect(() => decodeClaims("not-a-jwt")).toThrow(/malformed/);
  });
});

describe("isExpired", () => {
  const base = decodeClaims(makeToken({ user_id: "u", exp: 1000 }));
  it("is true past exp", () => expect(isExpired(base, 2000)).toBe(true));
  it("is false before exp", () => expect(isExpired(base, 500)).toBe(false));
  it("is false when exp is absent", () =>
    expect(isExpired(decodeClaims(makeToken({ user_id: "u" })), 9e9)).toBe(false));
});
