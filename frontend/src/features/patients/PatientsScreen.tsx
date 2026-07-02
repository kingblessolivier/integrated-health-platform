import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Field } from "../../components/ui/Field";
import { registerPatient, searchPatients } from "../../lib/api/patients";
import { holdsCommand } from "../../lib/entitlements";

/** Patient search (PTSR) + register (PTRG). Each action is shown only if the user holds the
 * command; the server re-checks regardless. */
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
    return (
      <div className="card">
        <div className="empty">
          <div className="empty__icon">🔒</div>
          <div className="empty__title">No patient access</div>
          <div className="empty__hint">You don't hold the patient search or register commands.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid-2">
      {canSearch && (
        <div className="card">
          <h3 className="card__title">
            <span className="badge">PTSR</span> Search patients
          </h3>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              setSubmitted(q.trim());
            }}
          >
            <Field label="Name or national ID" value={q} onChange={(e) => setQ(e.target.value)} />
            <button type="submit" className="btn btn--primary">Search</button>
          </form>

          {results.isLoading && <p style={{ marginTop: "var(--s-4)" }}>Searching…</p>}
          {results.isError && <div className="alert alert--error">Search failed.</div>}
          {results.data &&
            (results.data.results.length === 0 ? (
              <div className="alert alert--info" style={{ marginTop: "var(--s-4)" }}>No matches.</div>
            ) : (
              <table className="table" style={{ marginTop: "var(--s-4)" }}>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>National ID</th>
                  </tr>
                </thead>
                <tbody>
                  {results.data.results.map((p) => (
                    <tr key={p.id}>
                      <td>{[p.given_name, p.family_name].filter(Boolean).join(" ") || "—"}</td>
                      <td>{p.nida_id ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ))}
        </div>
      )}

      {canRegister && (
        <div className="card">
          <h3 className="card__title">
            <span className="badge">PTRG</span> Register patient
          </h3>
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
            <button type="submit" className="btn btn--primary" disabled={register.isPending}>
              {register.isPending ? "Registering…" : "Register"}
            </button>
            {register.isError && (
              <div className="alert alert--error" role="alert">
                Registration failed (duplicate or out of scope).
              </div>
            )}
            {register.isSuccess && <div className="alert alert--success">Patient registered.</div>}
          </form>
        </div>
      )}
    </div>
  );
}
