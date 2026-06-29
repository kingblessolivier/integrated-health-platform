# 56 — Domain Class Diagram

The object-oriented design view of the core domain. Behaviour (methods) reflects the
commands of doc 03; structure aligns with the conceptual model (doc 55) and physical schema
(doc 48).

## Core domain

```mermaid
classDiagram
    class Tenant {
      +UUID id
      +String name
      +String kind
    }
    class Facility {
      +UUID id
      +String level
      +Location location
    }
    class Staff {
      +UUID id
      +String fullName
      +GeoScope geoScope
      +Sensitivity maxSensitivity
      +holds(command) bool
    }
    class Command {
      +String code
      +String domain
      +String action
    }
    class Patient {
      +UUID id
      +String nidaId
      +bool isTemporary
      +register(nida)
      +merge(other)
      +grantConsent(scope)
    }
    class Encounter {
      +UUID id
      +Status status
      +DateTime date
      +open()
      +addDiagnosis(icd)
      +placeOrder(type)
      +close()
    }
    class Prescription {
      +UUID id
      +String code
      +Signature signature
      +sign(staff)
      +verify()
    }
    class Dispense {
      +UUID id
      +int quantity
      +selectBatchFEFO()
      +splitPayment()
    }
    class Product {
      +UUID id
      +String atc
      +String fdaReg
    }
    class Stock {
      +UUID id
      +String batch
      +Date expiry
      +int quantity
      +decrement(qty)
    }
    class Transaction {
      +UUID id
      +Money total
      +issueEbmReceipt()
    }
    class Claim {
      +UUID id
      +Status status
      +scrub()
    }
    class AuditEntry {
      +String prevHash
      +String currentHash
      +append(action)
    }

    Tenant "1" --> "*" Facility
    Tenant "1" --> "*" Staff
    Staff "*" --> "*" Command
    Patient "1" --> "*" Encounter
    Encounter "1" --> "*" Prescription
    Prescription "1" --> "*" Dispense
    Product "1" --> "*" Stock
    Dispense "1" --> "1" Transaction
    Transaction "1" --> "0..1" Claim
    Dispense ..> Stock : decrements
    AuditEntry "*" ..> Staff : records
```

## Access-control classes

```mermaid
classDiagram
    class AccessRequest {
      +Staff actor
      +Command command
      +Resource target
      +authorize() bool
    }
    class FourAxisPolicy {
      +checkRole(actor, command) bool
      +checkGeography(actor, target) bool
      +checkTenant(actor, target) bool
      +checkSensitivity(actor, target) bool
    }
    class ConsentPolicy {
      +isPermitted(patient, actor) bool
    }
    AccessRequest --> FourAxisPolicy
    AccessRequest --> ConsentPolicy
```

## Design notes
- **Capability-based:** `Staff.holds(command)` drives both authorisation and UI rendering —
  there is no per-role screen class.
- **Authorisation** is a pipeline: `FourAxisPolicy` (role · geo · tenant · sensitivity) then
  `ConsentPolicy`. A failure short-circuits to 403 and an `AuditEntry`.
- **Immutability:** `AuditEntry.append()` is the only write path; no update/delete methods.
