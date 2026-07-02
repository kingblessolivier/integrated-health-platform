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
  const [info, setInfo] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setBusy(true);
    try {
      const { access } = await login(nidaId, password, mfa ? otp : undefined);
      setToken(access);
    } catch (err) {
      if (err instanceof MfaRequiredError) {
        setMfa(true);
        setInfo("Enter the 6-digit code from your authenticator app.");
      } else {
        setError(err instanceof Error ? err.message : "Login failed.");
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login">
      <div className="login__card">
        <div className="login__brand">
          <span className="login__mark">🏥</span>
          <span>Integrated National Health Platform</span>
        </div>
        <p className="login__sub">Sign in to your account</p>

        {logoutReason === "expired" && (
          <div className="alert alert--warn">Your session expired — please sign in again.</div>
        )}
        {logoutReason === "scope_violation" && (
          <div className="alert alert--error">Session ended: access was out of scope.</div>
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
          {info && <div className="alert alert--info">{info}</div>}
          {error && (
            <div className="alert alert--error" role="alert">
              {error}
            </div>
          )}
          <button type="submit" className="btn btn--primary btn--block" disabled={busy}>
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
