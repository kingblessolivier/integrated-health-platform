import type { InputHTMLAttributes } from "react";

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

/** Labelled input using the design tokens (docs/05). */
export function Field({ label, id, ...rest }: FieldProps) {
  const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-");
  return (
    <label htmlFor={inputId} style={{ display: "block", marginBottom: "var(--space)" }}>
      <span style={{ display: "block", fontSize: 13, color: "var(--color-text-secondary)" }}>
        {label}
      </span>
      <input
        id={inputId}
        style={{
          width: "100%",
          padding: 8,
          border: "1px solid var(--color-border-strong)",
          borderRadius: "var(--radius)",
          fontFamily: "inherit",
        }}
        {...rest}
      />
    </label>
  );
}
