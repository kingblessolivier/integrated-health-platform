import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { Field } from "../../components/ui/Field";
import { mfaConfirm, mfaEnrol, type EnrolResult } from "../../lib/api/auth";

/** Self-service MFA enrolment (tier 2): enrol → show the secret + otpauth URI to add to an
 * authenticator app → confirm with a code. After confirming, login will require the OTP. */
export function MfaScreen() {
  const [enrolment, setEnrolment] = useState<EnrolResult | null>(null);
  const [otp, setOtp] = useState("");
  const [done, setDone] = useState(false);

  const enrol = useMutation({ mutationFn: mfaEnrol, onSuccess: setEnrolment });
  const confirm = useMutation({
    mutationFn: () => mfaConfirm(otp),
    onSuccess: () => setDone(true),
  });

  if (done) {
    return (
      <div className="card" style={{ maxWidth: 520 }}>
        <div className="empty">
          <div className="empty__icon">✅</div>
          <div className="empty__title">Two-factor authentication is active</div>
          <div className="empty__hint">You'll be asked for a code from your app at every sign-in.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="card" style={{ maxWidth: 520 }}>
      <h3 className="card__title">Set up two-factor authentication</h3>
      {!enrolment ? (
        <>
          <p className="card__subtitle">
            Generate a secret, add it to an authenticator app (Google Authenticator, Authy…), then
            confirm a code to activate.
          </p>
          <button className="btn btn--primary" onClick={() => enrol.mutate()} disabled={enrol.isPending}>
            {enrol.isPending ? "Generating…" : "Begin enrolment"}
          </button>
          {enrol.isError && (
            <div className="alert alert--error" role="alert">
              Could not start enrolment — you may already be enrolled. Ask an administrator to reset.
            </div>
          )}
        </>
      ) : (
        <>
          <div className="alert alert--info">Add this account to your authenticator app, then confirm below.</div>
          <table className="kv" style={{ marginBottom: "var(--s-4)" }}>
            <tbody>
              <tr>
                <td>Secret</td>
                <td><code>{enrolment.secret}</code></td>
              </tr>
              <tr>
                <td>otpauth URI</td>
                <td style={{ wordBreak: "break-all" }}>
                  <a href={enrolment.otpauth_uri}>{enrolment.otpauth_uri}</a>
                </td>
              </tr>
            </tbody>
          </table>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              confirm.mutate();
            }}
          >
            <Field
              label="Enter the 6-digit code to confirm"
              inputMode="numeric"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
            />
            <button type="submit" className="btn btn--primary" disabled={confirm.isPending}>
              {confirm.isPending ? "Confirming…" : "Confirm & activate"}
            </button>
            {confirm.isError && (
              <div className="alert alert--error" role="alert">
                Invalid code — try the current one from your app.
              </div>
            )}
          </form>
        </>
      )}
    </div>
  );
}
