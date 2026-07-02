import type { ActionSpec, FieldSpec } from "./types";

export interface BuiltRequest {
  method: "GET" | "POST";
  path: string;
  body?: Record<string, unknown>;
}

const PATH_PARAM = /\{(\w+)\}/g;

export function pathParamNames(path: string): string[] {
  return [...path.matchAll(PATH_PARAM)].map((m) => m[1]);
}

function coerce(field: FieldSpec, raw: string): unknown {
  if (field.type === "number") return raw === "" ? undefined : Number(raw);
  if (field.type === "json") return raw.trim() === "" ? undefined : JSON.parse(raw);
  return raw;
}

/**
 * Pure: turn an action spec + field values into a concrete request.
 * Path params fill `{name}` placeholders; remaining fields become the query string (GET)
 * or the JSON body (POST). Empty optional values are dropped. Throws on missing required
 * fields or invalid JSON so the runner can surface it before hitting the network.
 */
export function buildRequest(spec: ActionSpec, values: Record<string, string>): BuiltRequest {
  const pathParams = new Set(pathParamNames(spec.path));

  for (const f of spec.fields) {
    if (f.required && !values[f.name]?.trim()) {
      throw new Error(`${f.label} is required.`);
    }
  }

  let path = spec.path;
  for (const name of pathParams) {
    const v = values[name]?.trim();
    if (!v) throw new Error(`${name} is required.`);
    path = path.replace(`{${name}}`, encodeURIComponent(v));
  }

  const rest = spec.fields.filter((f) => !pathParams.has(f.name));

  if (spec.method === "GET") {
    const qs = new URLSearchParams();
    for (const f of rest) {
      const v = values[f.name]?.trim();
      if (v) qs.set(f.name, v);
    }
    const query = qs.toString();
    return { method: "GET", path: query ? `${path}?${query}` : path };
  }

  const body: Record<string, unknown> = {};
  for (const f of rest) {
    const raw = values[f.name] ?? "";
    if (raw.trim() === "" && !f.required) continue;
    const val = coerce(f, raw);
    if (val !== undefined) body[f.name] = val;
  }
  return { method: "POST", path, body };
}
