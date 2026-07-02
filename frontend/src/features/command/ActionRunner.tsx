import { useState } from "react";
import { Field } from "../../components/ui/Field";
import { api } from "../../lib/api/client";
import { buildRequest } from "../../lib/commands/request";
import type { ActionSpec, FieldSpec } from "../../lib/commands/types";

/** Renders a form from an ActionSpec, calls the endpoint via the shared api() client, and
 * shows the JSON result. One component drives every command-bound endpoint (docs/03, docs/49). */
export function ActionRunner({ spec }: { spec: ActionSpec }) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [result, setResult] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  // Reset transient state whenever the selected command changes.
  const [lastId, setLastId] = useState(spec.id);
  if (lastId !== spec.id) {
    setLastId(spec.id);
    setValues({});
    setResult(null);
    setError(null);
  }

  function set(name: string, v: string) {
    setValues((prev) => ({ ...prev, [name]: v }));
  }

  async function run(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    let req;
    try {
      req = buildRequest(spec, values);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid input.");
      return;
    }
    setBusy(true);
    try {
      const data = await api(req.path, {
        method: req.method,
        ...(req.body ? { body: JSON.stringify(req.body) } : {}),
      });
      setResult(data);
    } catch (err) {
      setError(renderError(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section style={{ maxWidth: 560 }}>
      <h3>
        <kbd>{spec.command}</kbd> {spec.label}
      </h3>
      <p style={{ color: "var(--color-text-secondary)", fontSize: 13 }}>
        {spec.method} <code>/api/v1{spec.path}</code>
      </p>
      <form onSubmit={run}>
        {spec.fields.map((f) => (
          <Input key={f.name} field={f} value={values[f.name] ?? ""} onChange={(v) => set(f.name, v)} />
        ))}
        <button
          type="submit"
          disabled={busy}
          style={{
            padding: "8px 16px",
            background: "var(--color-brand)",
            color: "#fff",
            border: "none",
            borderRadius: "var(--radius)",
            cursor: busy ? "default" : "pointer",
          }}
        >
          {busy ? "Running…" : spec.method === "GET" ? "Fetch" : "Submit"}
        </button>
      </form>

      {error && (
        <pre role="alert" style={{ color: "var(--color-danger)", whiteSpace: "pre-wrap" }}>
          {error}
        </pre>
      )}
      {result !== null && (
        <pre
          style={{
            background: "var(--color-surface)",
            border: "1px solid var(--color-border)",
            borderRadius: "var(--radius)",
            padding: 12,
            overflow: "auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </section>
  );
}

function Input({ field, value, onChange }: { field: FieldSpec; value: string; onChange: (v: string) => void }) {
  if (field.type === "select") {
    return (
      <label htmlFor={field.name} style={{ display: "block", marginBottom: "var(--space)" }}>
        <span style={{ display: "block", fontSize: 13, color: "var(--color-text-secondary)" }}>
          {field.label}
          {field.required ? " *" : ""}
        </span>
        <select
          id={field.name}
          value={value}
          required={field.required}
          onChange={(e) => onChange(e.target.value)}
          style={{ width: "100%", padding: 8, borderRadius: "var(--radius)", border: "1px solid var(--color-border-strong)" }}
        >
          <option value="">—</option>
          {field.options?.map((o) => (
            <option key={o} value={o}>
              {o}
            </option>
          ))}
        </select>
      </label>
    );
  }
  if (field.type === "textarea" || field.type === "json") {
    return (
      <label htmlFor={field.name} style={{ display: "block", marginBottom: "var(--space)" }}>
        <span style={{ display: "block", fontSize: 13, color: "var(--color-text-secondary)" }}>
          {field.label}
          {field.required ? " *" : ""}
        </span>
        <textarea
          id={field.name}
          value={value}
          required={field.required}
          placeholder={field.placeholder}
          onChange={(e) => onChange(e.target.value)}
          rows={field.type === "json" ? 3 : 2}
          style={{
            width: "100%",
            padding: 8,
            borderRadius: "var(--radius)",
            border: "1px solid var(--color-border-strong)",
            fontFamily: field.type === "json" ? "monospace" : "inherit",
          }}
        />
      </label>
    );
  }
  return (
    <Field
      label={field.required ? `${field.label} *` : field.label}
      id={field.name}
      type={field.type === "number" ? "number" : field.type === "date" ? "date" : "text"}
      inputMode={field.type === "number" ? "numeric" : undefined}
      value={value}
      placeholder={field.placeholder}
      required={field.required}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

function renderError(err: unknown): string {
  if (err && typeof err === "object" && "error" in err) {
    return JSON.stringify((err as { error: unknown }).error, null, 2);
  }
  if (err instanceof Error) return err.message;
  return "Request failed.";
}
