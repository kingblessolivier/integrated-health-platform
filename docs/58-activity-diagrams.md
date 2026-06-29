# 58 — Activity Diagrams

Workflow (process) view of key end-to-end activities, including decision points and parallel
paths. Complements the sequence diagrams in [57](57-sequence-diagrams.md).

## Outpatient visit (registration → dispensing)

```mermaid
flowchart TD
    Start([Patient arrives]) --> Reg[Register / verify via NIDA]
    Reg --> Elig{Insurance<br/>eligible?}
    Elig -- yes --> Enc[Open encounter]
    Elig -- no --> Cash[Flag out-of-pocket] --> Enc
    Enc --> Dx[Examine & record ICD diagnosis]
    Dx --> Need{Medication<br/>needed?}
    Need -- no --> Close[Close encounter] --> End([End])
    Need -- yes --> Rx[Sign prescription] --> SMS[/SMS code to patient/]
    SMS --> Disp[Pharmacy: verify + FEFO dispense]
    Disp --> Pay[Split insurer / collect MoMo]
    Pay --> Receipt[Issue EBM receipt] --> Close
```

## Dispensing with FEFO & validation

```mermaid
flowchart TD
    A([Enter Rx code / walk-in]) --> B[Scan product barcode]
    B --> C{In registered<br/>catalogue?}
    C -- no --> R1[Reject item] --> A
    C -- yes --> D[Select batch by FEFO]
    D --> E{Expired or<br/>insufficient?}
    E -- yes --> R2[Block dispense<br/>alert stock] --> A
    E -- no --> F[Split insurer / out-of-pocket]
    F --> G[Collect MoMo co-pay]
    G --> H{Payment<br/>confirmed?}
    H -- no --> G
    H -- yes --> I[Decrement stock]
    I --> J[Transmit EBM invoice]
    J --> K[Queue insurance claim]
    K --> L([Done + audit entry])
```

## CHW offline iCCM visit

```mermaid
flowchart TD
    S([Open app]) --> G{Inside village<br/>polygon? GPS}
    G -- no --> W[Warn: out of assigned area] --> S
    G -- yes --> T[Run iCCM decision tree]
    T --> RDT[Log RDT result]
    RDT --> Dose[Auto-calc dose by age/weight]
    Dose --> Kit[Decrement virtual kit]
    Kit --> Sev{Severe<br/>case?}
    Sev -- yes --> Ref[Create referral + SMS code]
    Sev -- no --> Rec[Record & advise]
    Ref --> Q[Queue to op-log]
    Rec --> Q
    Q --> Sync{Connectivity?}
    Sync -- no --> Q
    Sync -- yes --> Push[Sync + conflict check] --> E([End])
```

## Insurance claim lifecycle

```mermaid
flowchart LR
    A([Transaction]) --> B[Assemble claim batch]
    B --> C[AI scrubbing engine]
    C --> D{Flagged?}
    D -- no --> E[Auto-approve]
    D -- yes --> F[Auditor review]
    F --> G{Valid?}
    G -- yes --> E
    G -- no --> H[Reject + reason code]
    E --> I[Settle payment]
    I --> J([Reconciled])
    H --> J
```
