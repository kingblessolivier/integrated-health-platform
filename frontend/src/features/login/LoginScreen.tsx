import { useState } from "react";
import { Field } from "../../components/ui/Field";
import { login, MfaRequiredError } from "../../lib/api/auth";
import { useAuthStore } from "../../lib/auth/store";

/** Login → four-axis JWT. If the account has MFA, the first attempt returns mfa_required
 * and we reveal the OTP field, then resubmit with the code. */
export function LoginScreen() {
  const setToken = useAuthStore((s) => s.setToken);
  const logoutReason = useAuthStore((s) => s.logoutReason);
  const [nidaId, setNidaId] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [mfa, setMfa] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const { access } = await login(nidaId, password, mfa ? otp : undefined);
      setToken(access);
    } catch (err) {
      if (err instanceof MfaRequiredError) {
        setMfa(true);
        setError("Enter the 6-digit code from your authenticator app.");
      } else {
        setError(err instanceof Error ? err.message : "Login failed.");
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ maxWidth: 360, margin: "10vh auto", padding: 24 }}>
      <h1 style={{ color: "var(--color-brand-deep)", fontSize: 20 }}>
        🏥 Integrated National Health Platform
      </h1>
      {logoutReason === "expired" && (
        <p style={{ color: "var(--color-warning-fg)" }}>Your session expired — please sign in again.</p>
      )}
      {logoutReason === "scope_violation" && (
        <p style={{ color: "var(--color-danger)" }}>Session ended: access was out of scope.</p>
      )}
      <form onSubmit={submit}>
        <Field
          label="National ID"
          value={nidaId}
          autoComplete="username"
          onChange={(e) => setNidaId(e.target.value)}
          required
        />
        <Field
          label="Password"
          type="password"
          value={password}
          autoComplete="current-password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {mfa && (
          <Field
            label="Authenticator code"
            inputMode="numeric"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
          />
        )}
        {error && (
          <p role="alert" style={{ color: "var(--color-danger)", fontSize: 14 }}>
            {error}
          </p>
        )}
        <button
          type="submit"
          disabled={busy}
          style={{
            width: "100%",
            padding: 10,
            background: "var(--color-brand)",
            color: "#fff",
            border: "none",
            borderRadius: "var(--radius)",
            cursor: busy ? "default" : "pointer",
          }}
        >
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
