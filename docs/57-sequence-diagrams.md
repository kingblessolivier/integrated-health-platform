# 57 — Sequence Diagrams

Dynamic behaviour for the platform's most important interactions. Each aligns with a use
case in [53](53-use-case-model.md) and the API of [49](49-api-contract.md).

## Patient registration (NIDA)

```mermaid
sequenceDiagram
    actor Clerk
    participant API
    participant NIDA
    participant Core as Patient Core
    participant Audit
    Clerk->>API: POST /patients (PTRG, scan ID)
    API->>API: validate JWT scope (4-axis)
    API->>NIDA: verify(nida_id)
    alt NIDA available
        NIDA-->>API: demographics
    else circuit open
        API-->>Clerk: manual entry (deferred verify)
    end
    API->>Core: MPI duplicate check
    Core-->>API: unique / candidate
    API->>Core: create patient
    API->>Audit: append(PTRG)
    API-->>Clerk: 201 {patient_id}
```

## Prescribe → dispense → claim

```mermaid
sequenceDiagram
    actor Clinician
    actor Pharmacist
    participant API
    participant Stock
    participant RSSB
    participant EBM
    participant Audit
    Clinician->>API: POST /prescriptions (RXNW, signed)
    API->>API: validate ICD vs diagnosis
    API->>Audit: append(RXNW)
    API-->>Clinician: 201 {code}
    API-->>+Pharmacist: SMS code to patient
    Pharmacist->>API: POST /prescriptions/{code}/dispense (RXDP)
    API->>Stock: FEFO select & verify expiry
    Stock-->>API: batch ok
    API->>RSSB: eligibility + split
    RSSB-->>API: covered / co-pay
    API->>Stock: decrement
    API->>EBM: submit invoice
    EBM-->>API: certification token
    API->>Audit: append(RXDP)
    API-->>-Pharmacist: 201 {receipt}
```

## Emergency SOS dispatch

```mermaid
sequenceDiagram
    actor Patient
    participant SOS as Patient App
    participant SAMU
    participant Ambulance
    participant Hospital
    Patient->>SOS: tap SOS
    SOS->>SAMU: dispatch request + GPS
    SAMU->>SAMU: PostGIS nearest-unit query
    SAMU->>Ambulance: assignment + route
    Ambulance-->>Hospital: stream ECG/BP/SpO2
    SAMU->>Hospital: match + pre-alert
    Hospital-->>SAMU: accept (bed ready)
    Ambulance->>Hospital: arrival → handover into EMR
```

## Offline CHW visit & sync

```mermaid
sequenceDiagram
    actor CHW
    participant App as Mobile (offline)
    participant OpLog as Local op-log
    participant API
    participant Audit
    CHW->>App: open (GPS polygon check, cached)
    App->>App: iCCM tree, auto-dose, kit--
    App->>OpLog: append op (pending)
    Note over App,OpLog: works fully offline
    App->>API: on reconnect, push op (Idempotency-Key)
    alt no conflict
        API->>Audit: append(CHVS)
        API-->>App: 201 synced
    else version conflict
        API-->>App: 409
        App->>CHW: resolve (your vs server)
        CHW->>App: choose + reason
        App->>API: push resolution
    end
```

## Access denied (out of scope)

```mermaid
sequenceDiagram
    actor User
    participant API
    participant Policy as FourAxisPolicy
    participant Redis as JWT blacklist
    participant Audit
    User->>API: request (command X)
    API->>Policy: authorize(role,geo,tenant,sensitivity)
    Policy-->>API: deny
    API->>Redis: blacklist token
    API->>Audit: append(denied)
    API-->>User: 403 + session terminated
```
