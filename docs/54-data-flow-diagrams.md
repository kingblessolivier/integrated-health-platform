# 54 — Data Flow Diagrams (DFD)

Process view of how data moves through the platform, from the context level down to key
sub-processes. External systems are sources/sinks; the shared core is the central data store.

## Context diagram (Level 0)

```mermaid
flowchart TB
    Patient([Patient])
    Clinician([Clinical staff])
    Pharmacy([Pharmacy staff])
    CHW([Community health worker])
    Gov([District / National])
    NIDA[[NIDA]]
    INS[[RSSB / Insurers]]
    EBM[[RRA EBM]]
    HMIS[[DHIS2 / eIDSR]]
    SAMU[[SAMU 912]]
    MoMo[[Mobile Money]]

    P((0. Integrated National<br/>Health Platform))

    Patient -->|requests, consent, payment| P
    P -->|results, codes, bills| Patient
    Clinician -->|encounters, orders, diagnoses| P
    P -->|history, alerts| Clinician
    Pharmacy -->|dispense, stock, claims| P
    CHW -->|visits, referrals| P
    P -->|aggregated indicators| Gov
    P <-->|identity| NIDA
    P <-->|eligibility, claims| INS
    P -->|certified invoices| EBM
    P -->|FHIR bundles| HMIS
    P <-->|dispatch, telemetry| SAMU
    P <-->|collections| MoMo
```

## Level 1 — main processes

```mermaid
flowchart LR
    A([Actors]) --> P1[1. Identity &<br/>Access]
    P1 --> P2[2. Clinical<br/>Encounter]
    P2 --> P3[3. Pharmacy &<br/>Dispensing]
    P3 --> P4[4. Billing &<br/>Claims]
    P2 --> P5[5. Analytics &<br/>Reporting]
    P3 --> P5

    D1[(Patient record)]
    D2[(Medicine catalogue)]
    D3[(Inventory ledger)]
    D4[(Financial ledger)]
    D5[(Audit chain)]

    P1 <--> D1
    P2 <--> D1
    P3 <--> D2
    P3 <--> D3
    P4 <--> D4
    P1 --> D5
    P2 --> D5
    P3 --> D5
    P4 --> D5
    P5 --> HMIS[[DHIS2/eIDSR]]
    P4 --> EBM[[RRA EBM]]
    P1 <--> NIDA[[NIDA]]
    P4 <--> INS[[RSSB]]
```

## Level 2 — Process 3: Pharmacy & Dispensing

```mermaid
flowchart TB
    RX[/Prescription code/] --> P31[3.1 Verify<br/>prescription]
    P31 --> P32[3.2 FEFO batch<br/>selection]
    D3[(Inventory ledger)] <--> P32
    P32 --> P33[3.3 Split insurer /<br/>out-of-pocket]
    INS[[RSSB]] <--> P33
    P33 --> P34[3.4 Collect<br/>MoMo co-pay]
    MoMo[[Mobile Money]] <--> P34
    P34 --> P35[3.5 Decrement stock<br/>& issue EBM receipt]
    P35 --> D3
    P35 --> EBM[[RRA EBM]]
    P35 --> D4[(Financial ledger)]
    P35 --> D5[(Audit chain)]
```

## Notes
- Data stores correspond to the **shared core**: one patient record, one medicine catalogue,
  one inventory ledger, one financial ledger — plus the immutable audit chain.
- Every process writes to the audit chain (`D5`) for sensitive actions.
- External systems are reached through the resilience layer (circuit breaker) of doc 09.
