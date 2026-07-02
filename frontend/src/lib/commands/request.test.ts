import { describe, expect, it } from "vitest";
import { buildRequest } from "./request";
import type { ActionSpec } from "./types";

const post: ActionSpec = {
  id: "T", command: "T", label: "t", domain: "d", method: "POST",
  path: "/things/{id}/do/",
  fields: [
    { name: "id", label: "ID", required: true },
    { name: "name", label: "Name", required: true },
    { name: "count", label: "Count", type: "number" },
    { name: "meta", label: "Meta", type: "json" },
    { name: "opt", label: "Optional" },
  ],
};

const get: ActionSpec = {
  id: "G", command: "G", label: "g", domain: "d", method: "GET",
  path: "/search/", fields: [{ name: "q", label: "Q" }, { name: "limit", label: "Limit" }],
};

describe("buildRequest", () => {
  it("fills path params and builds a typed body", () => {
    const r = buildRequest(post, { id: "42", name: "x", count: "3", meta: '{"a":1}', opt: "" });
    expect(r).toEqual({
      method: "POST",
      path: "/things/42/do/",
      body: { name: "x", count: 3, meta: { a: 1 } },
    });
  });

  it("drops empty optional fields from the body", () => {
    const r = buildRequest(post, { id: "1", name: "y" });
    expect(r.body).toEqual({ name: "y" });
  });

  it("throws when a required field is missing", () => {
    expect(() => buildRequest(post, { id: "1" })).toThrow(/Name is required/);
  });

  it("throws when a required path param is missing", () => {
    expect(() => buildRequest(post, { name: "y" })).toThrow(/ID is required/);
  });

  it("throws on invalid JSON", () => {
    expect(() => buildRequest(post, { id: "1", name: "y", meta: "{bad" })).toThrow();
  });

  it("encodes path params", () => {
    const r = buildRequest(
      { ...post, fields: [{ name: "id", label: "ID", required: true }] },
      { id: "a b/c" },
    );
    expect(r.path).toBe("/things/a%20b%2Fc/do/");
  });

  it("builds a query string for GET and omits blanks", () => {
    const r = buildRequest(get, { q: "malaria", limit: "" });
    expect(r).toEqual({ method: "GET", path: "/search/?q=malaria" });
  });

  it("returns the bare path when no query values are given", () => {
    expect(buildRequest(get, {})).toEqual({ method: "GET", path: "/search/" });
  });
});
