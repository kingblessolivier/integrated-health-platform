/** Domain metadata for nav / tiles / palette grouping. Icons are text (docs/05: icon + label,
 * never colour/icon alone). Order controls nav + tile ordering. */
export const DOMAINS: { name: string; icon: string }[] = [
  { name: "Patients", icon: "👤" },
  { name: "Clinical", icon: "🩺" },
  { name: "Pharmacy", icon: "💊" },
  { name: "Diagnostics", icon: "🔬" },
  { name: "Stock", icon: "📦" },
  { name: "Supply", icon: "🚚" },
  { name: "Billing", icon: "💳" },
  { name: "Claims", icon: "📄" },
  { name: "CBHI", icon: "🛡️" },
  { name: "Community", icon: "🏘️" },
  { name: "Emergency", icon: "🚑" },
  { name: "Maternity", icon: "🤰" },
  { name: "Regulatory", icon: "⚖️" },
  { name: "PBF", icon: "📈" },
  { name: "Workforce", icon: "🧑‍⚕️" },
  { name: "Surveillance", icon: "🗺️" },
  { name: "Security", icon: "🔐" },
];

const ICON = new Map(DOMAINS.map((d) => [d.name, d.icon]));
export const domainIcon = (name: string) => ICON.get(name) ?? "•";
export const domainOrder = (name: string) => {
  const i = DOMAINS.findIndex((d) => d.name === name);
  return i === -1 ? DOMAINS.length : i;
};
