import { useState } from "react";
import { api } from "../../lib/api/client";
import { buildRequest } from "../../lib/commands/request";
import type { ActionSpec, FieldSpec } from "../../lib/commands/types";

/** Renders a form from an ActionSpec, calls the endpoint via the shared api() client, and
 * shows the result. One component drives every command-bound endpoint (docs/03, docs/49). */
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
    <div className="card">
      <div style={{ display: "flex", alignItems: "center", gap: "var(--s-2)" }}>
        <span className="badge">{spec.command}</span>
        <h3 className="card__title" style={{ margin: 0 }}>{spec.label}</h3>
        <span className={`method method--${spec.method}`} style={{ marginLeft: "auto" }}>
          {spec.method}
        </span>
      </div>
      <p className="card__subtitle" style={{ marginTop: "var(--s-2)" }}>
        <code>/api/v1{spec.path}</code>
      </p>

      <form onSubmit={run}>
        {spec.fields.length === 0 && (
          <p style={{ color: "var(--color-text-secondary)", fontSize: 13 }}>
            No inputs — just run it.
          </p>
        )}
        {spec.fields.map((f) => (
          <Input key={f.name} field={f} value={values[f.name] ?? ""} onChange={(v) => set(f.name, v)} />
        ))}
        <button type="submit" className="btn btn--primary" disabled={busy}>
          {busy ? "Running…" : spec.method === "GET" ? "Fetch" : "Submit"}
        </button>
      </form>

      {error && (
        <div className="alert alert--error" role="alert">
          <pre style={{ margin: 0, whiteSpace: "pre-wrap", font: "inherit" }}>{error}</pre>
        </div>
      )}
      {result !== null && <Result data={result} />}
    </div>
  );
}

function Result({ data }: { data: unknown }) {
  if (Array.isArray(data)) {
    return (
      <div style={{ marginTop: "var(--s-4)" }}>
        <div className="alert alert--success">{data.length} result(s).</div>
        {data.map((row, i) => (
          <ObjectTable key={i} obj={row} />
        ))}
      </div>
    );
  }
  if (data && typeof data === "object") {
    // Common list envelopes: {results: [...]} / {items: [...]}
    const env = data as Record<string, unknown>;
    const listKey = ["results", "items", "alerts"].find((k) => Array.isArray(env[k]));
    return (
      <div style={{ marginTop: "var(--s-4)" }}>
        <div className="alert alert--success">Success.</div>
        {listKey ? <Result data={env[listKey]} /> : <ObjectTable obj={data} />}
      </div>
    );
  }
  return (
    <div style={{ marginTop: "var(--s-4)" }}>
      <div className="alert alert--success">{String(data)}</div>
    </div>
  );
}

function ObjectTable({ obj }: { obj: unknown }) {
  if (!obj || typeof obj !== "object") {
    return <div className="alert alert--info">{String(obj)}</div>;
  }
  const entries = Object.entries(obj as Record<string, unknown>);
  return (
    <table className="kv" style={{ marginBottom: "var(--s-3)" }}>
      <tbody>
        {entries.map(([k, v]) => (
          <tr key={k}>
            <td>{k}</td>
            <td>
              {v !== null && typeof v === "object" ? (
                <code>{JSON.stringify(v)}</code>
              ) : (
                String(v)
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function Input({ field, value, onChange }: { field: FieldSpec; value: string; onChange: (v: string) => void }) {
  const labelEl = (
    <span className="field__label">
      {field.label}
      {field.required && <span className="field__req"> *</span>}
    </span>
  );
  if (field.type === "select") {
    return (
      <label htmlFor={field.name} className="field">
        {labelEl}
        <select
          id={field.name}
          className="select"
          value={value}
          required={field.required}
          onChange={(e) => onChange(e.target.value)}
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
      <label htmlFor={field.name} className="field">
        {labelEl}
        <textarea
          id={field.name}
          className={`textarea${field.type === "json" ? " textarea--mono" : ""}`}
          value={value}
          required={field.required}
          placeholder={field.placeholder}
          onChange={(e) => onChange(e.target.value)}
          rows={field.type === "json" ? 3 : 2}
        />
      </label>
    );
  }
  return (
    <label htmlFor={field.name} className="field">
      {labelEl}
      <input
        id={field.name}
        className="input"
        type={field.type === "number" ? "number" : field.type === "date" ? "date" : "text"}
        inputMode={field.type === "number" ? "numeric" : undefined}
        value={value}
        placeholder={field.placeholder}
        required={field.required}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}

function renderError(err: unknown): string {
  if (err && typeof err === "object" && "error" in err) {
    return JSON.stringify((err as { error: unknown }).error, null, 2);
  }
  if (err instanceof Error) return err.message;
  return "Request failed.";
}
