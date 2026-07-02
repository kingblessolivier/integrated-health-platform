# 49 — API Contract

How clients talk to the platform. Endpoints follow the three access tiers of doc 04 —
public (`/auth/token`, refresh, health), authenticated-no-command (own profile, reference
data, MFA enrolment), and command-gated, where the endpoint maps to exactly one **command**
(doc 03) under the four-axis model. This is the contract dev teams build against; the
canonical machine-readable spec is an **OpenAPI 3.1** document generated from the
Django REST / FastAPI serializers.

## Conventions

- Base path: `/api/v1`. Versioning policy: [38 — API Versioning](38-api-versioning-and-deprecation.md).
- Auth: `Authorization: Bearer <JWT>` (RS256) on every request. The JWT carries
  `role/commands`, `geo_scope`, `tenant_id`, `max_sensitivity`.
- Command binding: a **command-gated** request resolves to a command code; the server checks
  the caller **holds** it before executing. Missing → `403`, session terminated, token
  blacklisted, event logged. Tier-2 endpoints need only a valid token.
- MFA: `POST /auth/mfa/enrol/` mints a TOTP secret (returns `secret` + `otpauth_uri`; `409`
  if already enrolled — admin reset required); `POST /auth/mfa/confirm/` `{otp}` proves the
  authenticator and activates enforcement. From then on `POST /auth/token/` requires `otp`
  alongside the credentials, else `401 mfa_required`.
- Content type: `application/json`; resource names plural kebab-case (`/stock-items`).
- Idempotency: unsafe writes accept an `Idempotency-Key` header (critical for offline replay).
- Pagination: cursor-based — `?limit=&cursor=`; responses include `next_cursor`.
- Correlation: every request/response carries `X-Correlation-Id`
  ([37 — Observability](37-observability-correlation-and-tracing.md)).

## Standard error envelope

```json
{
  "error": {
    "code": "DUPLICATE_PATIENT",
    "message": "A patient with this NIDA already exists.",
    "command": "PTRG",
    "correlation_id": "9f1c…",
    "details": { "patient_id": "uuid" }
  }
}
```

| HTTP | When |
|---|---|
| `400` | Validation failure (see [47 — Validation Rules](47-validation-rules.md)) |
| `401` | Missing/expired token |
| `403` | Caller does not hold the command, or out of geo/tenant/sensitivity scope |
| `404` | Resource not found / NIDA lookup miss |
| `409` | Conflict (duplicate, version mismatch on offline replay) |
| `422` | Business-rule rejection (e.g. dispensing an expired batch) |
| `429` | Rate limit ([42 — Rate Limiting](42-rate-limiting-and-quotas.md)) |
| `503` | Downstream national system open-circuit; degraded mode |

## OpenAPI excerpt

```yaml
openapi: 3.1.0
info: { title: Integrated National Health Platform API, version: "1.0" }
servers: [{ url: /api/v1 }]
components:
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
security: [{ bearerAuth: [] }]
paths:
  /patients:
    post:
      summary: Register patient (NIDA auto-fill)
      x-command: PTRG
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/PatientRegister' }
      responses:
        '201': { description: Created, content: { application/json: { schema: { $ref: '#/components/schemas/Patient' }}}}
        '403': { description: Caller lacks PTRG or is out of scope }
        '409': { description: Duplicate patient (master patient index) }
    get:
      summary: Search patients
      x-command: PTSR
      parameters:
        - { name: q, in: query, schema: { type: string }}
        - { name: limit, in: query, schema: { type: integer, default: 25 }}
        - { name: cursor, in: query, schema: { type: string }}
      responses:
        '200': { description: OK }

  /encounters:
    post:
      summary: Open encounter
      x-command: ENNW
      responses: { '201': { description: Created }, '403': { description: Forbidden }}

  /encounters/{id}/diagnoses:
    post:
      summary: Record ICD-coded diagnosis
      x-command: ENDX
      responses: { '201': { description: Created }, '422': { description: ICD invalid for diagnosis }}

  /prescriptions:
    post:
      summary: Prescribe (digital sign)
      x-command: RXNW
      responses: { '201': { description: Created }}

  /prescriptions/{code}/dispense:
    post:
      summary: Dispense under FEFO (barcode-verified)
      x-command: RXDP
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                batch_barcode: { type: string }
                quantity: { type: integer }
                payment_split: { $ref: '#/components/schemas/PaymentSplit' }
      responses:
        '201': { description: Dispensed; EBM receipt issued }
        '422': { description: Expired/empty batch, or FEFO violation }

components:
  schemas:
    PatientRegister:
      type: object
      required: [nida_id]
      properties:
        nida_id: { type: string }
        given_name: { type: string }
        family_name: { type: string }
        sex: { type: string, enum: [male, female] }
        birth_date: { type: string, format: date }
    Patient:
      allOf:
        - { $ref: '#/components/schemas/PatientRegister' }
        - type: object
          properties: { id: { type: string, format: uuid }, audit_id: { type: string }}
    PaymentSplit:
      type: object
      properties:
        insurer_portion: { type: number }
        out_of_pocket: { type: number }
        momo_request_id: { type: string }
```

## Streaming endpoints

High-frequency vitals (ambulance, anaesthesia) do **not** use REST:

- **WebSocket** (Django Channels) — `wss://…/ws/vitals/{encounter_id}` for ECG/BP/SpO₂.
- **gRPC over HTTP/2** for the anaesthesia workstation.

See [07 — Technology Stack](07-technology-stack.md) and
[19 — Ambulance & Emergency Management](19-ambulance-and-emergency-management.md).
