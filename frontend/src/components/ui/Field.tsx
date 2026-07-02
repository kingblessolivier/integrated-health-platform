import type { InputHTMLAttributes } from "react";

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  required?: boolean;
}

/** Labelled input using the design tokens (docs/05). */
export function Field({ label, id, required, ...rest }: FieldProps) {
  const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-");
  return (
    <label htmlFor={inputId} className="field">
      <span className="field__label">
        {label}
        {required && <span className="field__req"> *</span>}
      </span>
      <input id={inputId} className="input" required={required} {...rest} />
    </label>
  );
}
