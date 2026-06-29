# 62 — Requirements Traceability Matrix

Links each functional requirement ([52 — SRS](52-software-requirements-specification.md)) to
its use case, design artifacts, and the test type that verifies it. This is the backbone for
verifying that every requirement is designed and tested.

## Functional requirements

| Req | Use case | Command(s) | Design artifacts | Verified by |
|---|---|---|---|---|
| FR-01 Register patient (NIDA) | UC-01 | `PTRG`,`PTTM` | 48 schema, 49 API, 57 seq | Integration (NIDA stub), E2E |
| FR-02 Longitudinal record / MPI | UC-01 | `PTSR`,`PTVW`,`PTMG` | 48, 55, 61 | Unit (dedup), E2E |
| FR-03 Encounter capture | UC-02 | `ENNW`,`ENVT`,`ENDX` | 56 class, 59 state | Unit, E2E |
| FR-04 CPOE orders | UC-02 | `LBOR`,`ENDX` | 49 API, 57 | Integration |
| FR-05 Prescribe (signed) | UC-04 | `RXNW` | 47 validation, 57 seq | Unit (ICD check), E2E |
| FR-06 Dispense FEFO + split | UC-05 | `RXVF`,`RXDP` | 48 (FEFO idx), 58 activity | Unit (FEFO), E2E |
| FR-07 EBM certified invoice | UC-05 | `RXDP` | 09 interop, 36 payments | Integration (EBM stub) |
| FR-08 Inventory & alerts | — | `STVW`,`STAL` | 48, 16 | Unit, integration |
| FR-09 B2B marketplace | — | `PObm`,`POrc` | 17 supply chain | Integration |
| FR-10 CHW offline iCCM | UC-10 | `CHVS`,`CHRF` | 51 mobile, 58 activity | Unit (polygon), device test |
| FR-11 Emergency dispatch | UC-11 | `EMSO`,`EMDP` | 57 seq, 60 deploy | Integration (PostGIS), E2E |
| FR-12 Insurance claims | UC-05 | `CLSB`,`CLrv` | 58 activity, 59 state | Integration (RSSB stub) |
| FR-13 HR & payroll | — | `HRon`,`PRrn` | 18 HR | Unit, integration |
| FR-14 Consent | — | `CNGR`,`CNRV` | 56 (ConsentPolicy) | Unit, security test |
| FR-15 Command-driven access | all | (all) | 04, 50 frontend | Unit (entitlements), E2E |
| FR-16 Four-axis scoping | all | (all) | 04, 56, 57 (deny) | Security test, unit |
| FR-17 Dashboards/analytics | — | `ANVW` | 14 analytics, 06 | E2E, visual |
| FR-18 FHIR to DHIS2/eIDSR | — | (scheduled) | 09 interop | Integration (FHIR validate) |
| FR-19 Audit chain | all | (all) | 48, 34 | Unit (hash chain), security |
| FR-20 Offline sync | UC-10 | (sync) | 51, 28, 59 | Unit (conflict), device test |
| FR-21 Patient portal/USSD | — | `PTFC`,`APbk` | 49, 50 | E2E |

## Non-functional requirements

| Req | Design artifacts | Verified by |
|---|---|---|
| NFR-01/02 Performance | 25 load balancing, 24 indexing | Load test against targets |
| NFR-03 Availability | 60 deploy, 31 backup/DR | Failover drill, chaos test |
| NFR-04 Scalability | 25, 60 | Surge load test |
| NFR-05 Security | 08, 32, 39 | Pen test, dependency scan |
| NFR-06 Privacy | 13 visibility, 33 compliance | Data-minimisation review |
| NFR-07 Compliance | 33, 34 | Compliance audit |
| NFR-08 Usability | 05 design, 50 | WCAG (axe) + field usability |
| NFR-09 Reliability | 27 resilience, 09 | Circuit-breaker test |
| NFR-10 Interoperability | 09, 38 | FHIR/EBM conformance |
| NFR-11 Maintainability | 23, 43 | CI/CD pipeline checks |
| NFR-12 Observability | 30, 37 | Trace/alert verification |

## Coverage summary
- Every **Must** functional requirement traces to at least one use case, design artifact, and
  test type.
- Command codes marked illustratively (e.g. `CHVS`, `EMSO`) extend the catalogue in
  [03](03-command-catalogue.md) and should be reconciled there as those domains are finalised.
