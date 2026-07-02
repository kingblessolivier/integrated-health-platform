import { describe, expect, it } from "vitest";
import { actionById, ACTIONS } from "./registry";
import { pathParamNames } from "./request";

describe("command registry", () => {
  it("has unique action ids", () => {
    const ids = ACTIONS.map((a) => a.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("every path param has a matching field", () => {
    for (const a of ACTIONS) {
      const fields = new Set(a.fields.map((f) => f.name));
      for (const p of pathParamNames(a.path)) {
        expect(fields.has(p), `${a.id} missing field for {${p}}`).toBe(true);
      }
    }
  });

  it("every action path is rooted and every command is 4 chars", () => {
    for (const a of ACTIONS) {
      expect(a.path.startsWith("/")).toBe(true);
      expect(a.command).toMatch(/^[A-Z]{4}$/);
    }
  });

  it("select fields declare options", () => {
    for (const a of ACTIONS) {
      for (const f of a.fields) {
        if (f.type === "select") expect(f.options?.length).toBeGreaterThan(0);
      }
    }
  });

  it("looks up by id", () => {
    expect(actionById("PTRG")?.label).toBe("Register patient");
    expect(actionById("nope")).toBeUndefined();
  });
});
