# 21 — Threat Monitoring & Incident Response

## Security operations centre (SOC)

- A **24/7 SOC** monitors the platform's security posture from a central dashboard.
- Live metrics: active sessions, failed authentication attempts, anomalous access patterns,
  WAF events, infrastructure alerts.
- Alerts are triaged by severity: **critical (immediate), high (1 hour), medium (24 hours)**.

## Threat detection

- The **WAF** inspects every incoming request; malicious payloads are dropped at the edge.
- The **anomaly-detection engine** flags unusual patterns: off-hours record access, sudden
  export spikes, geographic-scope violations.
- **Brute-force detection:** repeated failed logins trigger progressive delays and account
  lock.
- The AI claims-scrubbing engine also serves as a **fraud-detection** layer.

## Incident containment & response

- **`LOCK` command:** the compromised account's session is terminated, its JWT blacklisted in
  Redis, and the account locked in the database — all within seconds.
- Response flow: **Detection → Assessment → Containment → Eradication → Recovery →
  Post-incident report** (reconstructed from the audit chain).
- If patient data is confirmed compromised, the **National Cybersecurity Authority** and the
  **data-protection regulator** are notified within the legally required timeframe.

## Penetration testing & vulnerability management

- Scheduled penetration tests by an **independent security firm**, minimum annually.
- Vulnerability scanning of all containers and dependencies on every deployment.
- **Critical / high** vulnerabilities patched within **48 hours**; **medium** within
  **14 days**.
