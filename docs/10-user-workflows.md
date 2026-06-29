# 10 — User Workflows

What each actor actually *does* in the system. Every workflow writes to the shared
core, so the next authorised actor reads the result without re-keying.

## Community health workers (*binôme*)

- Open the offline-first app; **GPS verifies** the CHW is inside their assigned village polygon.
- Record sick-child symptoms through guided **iCCM decision trees** (malaria, diarrhoea,
  pneumonia, malnutrition).
- Log RDT results; the system auto-calculates the dose from age and weight and decrements
  the **virtual health kit**.
- Trigger a referral for severe cases; a **six-digit tracking code** is sent to the parent
  by SMS.
- Record family planning, contraceptive provision, TB DOT, and NCD prevention. Data syncs
  when connectivity returns.

## ASM — maternal & newborn CHW

- Register pregnancies and schedule antenatal follow-up visits.
- Record danger signs at each visit and promote facility delivery.
- Log delivery at facility and record postnatal follow-up of mother and newborn.

## Health centre & sector staff

- Receive referred patients via the tracking code; the **full CHW assessment loads instantly**.
- Conduct triage, clinical consultation, and order laboratory tests.
- Dispense from the health-centre dispensary against the **shared inventory**.
- Monthly indicator reports are generated automatically from care events — **no extra form**.
- Evaluate CHW cooperative performance and submit PBF payment requests.

## Hospital clinical staff

| Role | What they do |
|---|---|
| Reception / ADT clerk | Scan national ID, verify via NIDA, check insurance eligibility, open encounter |
| Clinician | Review longitudinal history, stream vitals, record ICD-coded diagnosis, place CPOE orders |
| Emergency physician | Activate **trauma override** for unidentified critical patients |
| Ward nurse | Check medication schedule, scan wristband + drug barcode, verify the **five rights**, record administration |
| Lab technologist | Scan specimen, run analyser, verify and sign results into the EMR |
| Radiologist | Review DICOM images, draft and **digitally sign** structured report |
| Anaesthetist | Stream high-frequency perioperative vitals, step through the surgical safety checklist |
| Midwife | Record delivery, register birth, initiate postnatal record |
| Mortuary officer | Record death with ICD-coded cause; feeds civil registration and mortality statistics |

## Pharmacy staff

- **Dispensing pharmacist:** enter the SMS prescription code or walk-in item, scan barcodes
  to verify batch and expiry under **FEFO**, split the transaction between insurer and
  patient, collect mobile-money co-payment, generate a **certified EBM receipt**.
- **Procurement officer:** monitor stock against safety thresholds, open the B2B
  marketplace, compare wholesaler catalogues, execute the purchase order, receive goods and
  log batch/expiry.
- **Owner:** open the daily dashboard for cash position, insurer receivables, expiry alerts,
  and margins.

## Patients & citizens

- View appointments, active prescriptions with redemption codes, lab results, and bills.
- Search for care by condition, filtered by insurance acceptance and estimated co-pay.
- Reserve a prescription at a chosen pharmacy; pay the co-payment by mobile money.
- Use the **AI first-aid assistant** in Kinyarwanda, French, or English; request SAMU 912
  with one tap.
- Grant or revoke consent for specific actors to view their record.
- Feature-phone users receive prescription codes and reminders, and can pay via USSD.

## Ambulance crew (paramedic / EMT)

- Receive the dispatch assignment with an optimised route on the vehicle tablet.
- Open the emergency case file on scene; attach the portable vitals monitor.
- Stream ECG, blood pressure, and SpO₂ continuously to the destination hospital.
- Record findings; the system selects the best receiving facility.
- **Handover:** the pre-hospital record flows into the hospital EMR without re-keying.

## SAMU 912 dispatch controller

- Receive requests from 912 calls, patient-app SOS (GPS auto-sent), or facility transfers.
- Dispatch the nearest available ambulance using live GPS proximity.
- Monitor fleet status and allocate vehicles across active incidents.
- Coordinate with receiving hospitals on bed availability.

## District & government users

- **District epidemiologist:** monitor real-time disease clusters; investigate alerts;
  coordinate outbreak response.
- **DHO:** review district performance against targets; manage inter-facility stock transfers.
- **District CBHI manager:** track enrolment, premiums, and fund balance.
- **Provincial coordinator:** compare districts; support lagging performers.
- **MoH / national:** review national indicators; push FHIR bundles to DHIS2 and eIDSR.

## Back-office administration

- **HR officer:** onboard staff using NIDA verification and professional-council licence
  check; generate digital contracts; manage transfers; revoke and grant access.
- **Payroll accountant:** run monthly payroll with PAYE and RSSB deductions; disburse salary
  advances within regulatory caps.
- **Claims officer:** submit claim batches; review AI-scrubbed disputes; track settlement.
- **IT / SOC analyst:** monitor security dashboards; respond to alerts; manage accounts;
  maintain the audit chain.
