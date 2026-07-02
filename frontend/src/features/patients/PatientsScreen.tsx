import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Field } from "../../components/ui/Field";
import { registerPatient, searchPatients } from "../../lib/api/patients";
import { holdsCommand } from "../../lib/entitlements";

/** Patient search (PTSR) + register (PTRG) — the first API-backed vertical slice. Each
 * action is shown only if the user holds the command; the server re-checks regardless. */
export function PatientsScreen() {
  const canSearch = holdsCommand("PTSR");
  const canRegister = holdsCommand("PTRG");
  const [q, setQ] = useState("");
  const [submitted, setSubmitted] = useState("");
  const qc = useQueryClient();

  const results = useQuery({
    queryKey: ["patients", submitted],
    queryFn: () => searchPatients(submitted),
    enabled: canSearch && submitted.length > 0,
  });

  const [form, setForm] = useState({ nida_id: "", given_name: "", family_name: "" });
  const register = useMutation({
    mutationFn: registerPatient,
    onSuccess: () => {
      setForm({ nida_id: "", given_name: "", family_name: "" });
      qc.invalidateQueries({ queryKey: ["patients"] });
    },
  });

  if (!canSearch && !canRegister) {
    return <p style={{ color: "var(--color-text-secondary)" }}>You don't have patient access.</p>;
  }

  return (
    <div style={{ display: "grid", gap: 24, gridTemplateColumns: "1fr 1fr", alignItems: "start" }}>
      {canSearch && (
        <section>
          <h3>Search patients (PTSR)</h3>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              setSubmitted(q.trim());
            }}
          >
            <Field label="Name or national ID" value={q} onChange={(e) => setQ(e.target.value)} />
          </form>
          {results.isLoading && <p>Searching…</p>}
          {results.isError && <p style={{ color: "var(--color-danger)" }}>Search failed.</p>}
          {results.data && (
            <ul>
              {results.data.results.map((p) => (
                <li key={p.id}>
                  {p.given_name} {p.family_name} <small>({p.nida_id})</small>
                </li>
              ))}
              {results.data.results.length === 0 && <li>No matches.</li>}
            </ul>
          )}
        </section>
      )}

      {canRegister && (
        <section>
          <h3>Register patient (PTRG)</h3>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              register.mutate(form);
            }}
          >
            <Field
              label="National ID"
              value={form.nida_id}
              onChange={(e) => setForm({ ...form, nida_id: e.target.value })}
              required
            />
            <Field
              label="Given name"
              value={form.given_name}
              onChange={(e) => setForm({ ...form, given_name: e.target.value })}
            />
            <Field
              label="Family name"
              value={form.family_name}
              onChange={(e) => setForm({ ...form, family_name: e.target.value })}
            />
            <button type="submit" disabled={register.isPending}>
              {register.isPending ? "Registering…" : "Register"}
            </button>
            {register.isError && (
              <p role="alert" style={{ color: "var(--color-danger)" }}>
                Registration failed (duplicate or out of scope).
              </p>
            )}
            {register.isSuccess && <p style={{ color: "var(--color-success)" }}>Patient registered.</p>}
          </form>
        </section>
      )}
    </div>
  );
}
