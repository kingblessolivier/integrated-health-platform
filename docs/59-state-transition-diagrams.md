# 59 — State Transition Diagrams

Lifecycle (state machine) view of the platform's key stateful entities. States and
transitions align with the domain model in [56](56-domain-class-diagram.md).

## Encounter

```mermaid
stateDiagram-v2
    [*] --> Open : ENNW
    Open --> InProgress : record vitals / diagnosis
    InProgress --> Ordered : place orders (lab/imaging/Rx)
    Ordered --> InProgress : results return
    InProgress --> Referred : refer out (tracking code)
    InProgress --> Closed : ENCL
    Referred --> Closed
    Closed --> [*]
```

## Prescription

```mermaid
stateDiagram-v2
    [*] --> Signed : RXNW (digital signature)
    Signed --> Verified : RXVF (pharmacist)
    Verified --> PartiallyDispensed : partial fill
    PartiallyDispensed --> Dispensed : remaining filled
    Verified --> Dispensed : RXDP (full)
    Signed --> Cancelled : RXCN
    Verified --> Expired : validity lapses
    Dispensed --> [*]
    Cancelled --> [*]
    Expired --> [*]
```

## Insurance claim

```mermaid
stateDiagram-v2
    [*] --> Submitted
    Submitted --> Scrubbing : AI engine
    Scrubbing --> Approved : clean
    Scrubbing --> Disputed : flagged
    Disputed --> Approved : auditor accepts
    Disputed --> Rejected : auditor rejects
    Approved --> Paid : settlement
    Paid --> [*]
    Rejected --> [*]
```

## Ambulance / dispatch

```mermaid
stateDiagram-v2
    [*] --> Available
    Available --> Dispatched : assignment
    Dispatched --> EnRoute : crew accepts
    EnRoute --> OnScene : arrival
    OnScene --> Transporting : patient loaded
    Transporting --> AtHospital : handover
    AtHospital --> Available : cleared
    Available --> Maintenance : service due
    Maintenance --> Available
```

## User account (access lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Provisioned : HR onboard (NIDA + licence)
    Provisioned --> Active : first login + MFA
    Active --> Locked : failed logins / LOCK command
    Locked --> Active : SOC unlock
    Active --> Transferred : reassign scope
    Transferred --> Active
    Active --> Deactivated : resignation / termination
    Deactivated --> [*]
```

## Offline sync (mobile record)

```mermaid
stateDiagram-v2
    [*] --> Pending : created offline
    Pending --> Syncing : connectivity restored
    Syncing --> Synced : 2xx
    Syncing --> Conflict : 409
    Conflict --> Syncing : user resolves
    Syncing --> Pending : 5xx (backoff)
    Synced --> [*]
```
