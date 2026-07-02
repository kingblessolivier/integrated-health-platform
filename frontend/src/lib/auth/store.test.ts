import { beforeEach, describe, expect, it } from "vitest";
import { useAuthStore } from "./store";

function makeToken(payload: Record<string, unknown>): string {
  const b64 = (o: unknown) =>
    btoa(JSON.stringify(o)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  return `${b64({ alg: "HS256", typ: "JWT" })}.${b64(payload)}.sig`;
}

describe("auth store", () => {
  beforeEach(() => {
    localStorage.clear();
    useAuthStore.getState().forceLogout("user");
  });

  it("sets the session and command set from a token", () => {
    useAuthStore.getState().setToken(makeToken({ user_id: "u-9", tenant_id: "t-9", commands: ["PTSR"] }));
    const s = useAuthStore.getState();
    expect(s.userId).toBe("u-9");
    expect(s.tenantId).toBe("t-9");
    expect(s.commands.has("PTSR")).toBe(true);
    expect(localStorage.getItem("inhp.token")).not.toBeNull();
  });

  it("clears everything on forceLogout and records the reason", () => {
    useAuthStore.getState().setToken(makeToken({ user_id: "u", commands: ["PTSR"] }));
    useAuthStore.getState().forceLogout("expired");
    const s = useAuthStore.getState();
    expect(s.token).toBeNull();
    expect(s.commands.size).toBe(0);
    expect(s.logoutReason).toBe("expired");
    expect(localStorage.getItem("inhp.token")).toBeNull();
  });
});
