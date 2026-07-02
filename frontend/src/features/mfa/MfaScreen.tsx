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
    return <p style={{ color: "var(--color-success)" }}>✅ MFA is now active on your account.</p>;
  }

  return (
    <section style={{ maxWidth: 480 }}>
      <h3>Set up two-factor authentication</h3>
      {!enrolment ? (
        <>
          <p style={{ color: "var(--color-text-secondary)" }}>
            Generate a secret, add it to an authenticator app (Google Authenticator, Authy…),
            then confirm a code to activate.
          </p>
          <button onClick={() => enrol.mutate()} disabled={enrol.isPending}>
            {enrol.isPending ? "Generating…" : "Begin enrolment"}
          </button>
          {enrol.isError && (
            <p role="alert" style={{ color: "var(--color-danger)" }}>
              Could not start enrolment (already enrolled? ask an administrator to reset).
            </p>
          )}
        </>
      ) : (
        <>
          <p>Add this account to your authenticator app:</p>
          <p>
            <strong>Secret:</strong> <code>{enrolment.secret}</code>
          </p>
          <p style={{ wordBreak: "break-all", fontSize: 12, color: "var(--color-text-secondary)" }}>
            <a href={enrolment.otpauth_uri}>{enrolment.otpauth_uri}</a>
          </p>
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
            <button type="submit" disabled={confirm.isPending}>
              {confirm.isPending ? "Confirming…" : "Confirm & activate"}
            </button>
            {confirm.isError && (
              <p role="alert" style={{ color: "var(--color-danger)" }}>
                Invalid code — try the current one from your app.
              </p>
            )}
          </form>
        </>
      )}
    </section>
  );
}
