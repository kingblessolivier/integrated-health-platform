/** Declarative description of a backend action, so one generic runner can drive every
 * command-bound endpoint (docs/03, docs/49) instead of a bespoke screen per route. */
export type FieldType = "text" | "number" | "date" | "select" | "textarea" | "json";

export interface FieldSpec {
  name: string;
  label: string;
  type?: FieldType; // default "text"
  required?: boolean;
  options?: string[]; // for select
  placeholder?: string;
}

export interface ActionSpec {
  /** Stable unique id (some commands, e.g. PTVW, back more than one action). */
  id: string;
  /** Command code the caller must hold (entitlement + audit key). */
  command: string;
  label: string;
  domain: string;
  method: "GET" | "POST";
  /** Path under /api/v1, may contain {param} placeholders filled from same-named fields. */
  path: string;
  fields: FieldSpec[];
  description?: string;
}
