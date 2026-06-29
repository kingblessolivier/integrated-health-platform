# Security Policy

The Integrated National Health Platform handles sensitive personal health data. Security
and privacy are treated as first-class concerns. This document explains how to report a
vulnerability and what is in scope.

> **Note:** This repository currently holds the **documentation and design specification**.
> The security model it describes is detailed in
> [docs/08 — Security & Cryptography](docs/08-security-and-cryptography.md) and
> [docs/21 — Threat Monitoring & Incident Response](docs/21-threat-monitoring-and-incident-response.md).

## Reporting a vulnerability

**Please do not open a public issue for security vulnerabilities.**

Instead, report privately using one of:

- GitHub's **private vulnerability reporting** — the *Security* tab → *Report a
  vulnerability* (preferred).
- Contacting a project maintainer directly through a private channel.

When reporting, please include:

- A description of the issue and its potential impact.
- Steps to reproduce, or a proof of concept.
- Affected component, version, or document, and any suggested remediation.

## What to expect

- **Acknowledgement** of your report as soon as is practical.
- An assessment of severity and an indication of the planned remediation timeline.
- For documented platform vulnerabilities, remediation targets follow the policy in the
  docs: **critical / high within 48 hours, medium within 14 days.**
- Coordinated disclosure — we will agree a disclosure timeline with you and credit you if
  you wish.

## Scope

- **In scope:** issues in this repository's contents, and design weaknesses in the security
  model or access-control rules described here.
- **Out of scope:** vulnerabilities in third-party national systems (NIDA, DHIS2, RSSB/
  KWIVUZA, RRA EBM, SAMU, etc.) — please report those to the responsible operator.

## Handling sensitive data

Never include **real patient data, credentials, API keys, tokens, or `.env` contents** in a
report, issue, pull request, or screenshot. Use synthetic or redacted examples. See the
ground rules in [CONTRIBUTING.md](CONTRIBUTING.md).
