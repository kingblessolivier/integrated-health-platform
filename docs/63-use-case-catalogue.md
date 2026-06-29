# 63 — Use Case Catalogue — What Every User Can Do

A complete, role-by-role account of what every user of the Integrated National Health
Platform is able to do. Each capability is a **use case** backed by one or more **commands**
(the atomic units of access — see [03 — Command Catalogue](03-command-catalogue.md)) and
bounded by the **four-axis access model** (Role · Geography · Tenant · Sensitivity — see
[04](04-access-control-model.md)). What a user *cannot* see follows the visibility rules in
[13 — Data Visibility by Role](13-data-visibility-by-role.md).

## How to read this document

For each role you will find:

- **Mandate** — the role in one line.
- **Command bundle** — the preset pack of commands the role is provisioned with (doc 03).
- **What they can do** — a table of use cases → command(s) → what it lets them do.
- **Boundaries** — what the role explicitly *cannot* do or see.

> The command is the atom; bundles are convenience presets an admin applies and then tunes.
> Holding a command is what makes its use case appear in the unified dashboard and command
> bar. **`ANVW`** (the dashboard, rendered at the holder's altitude) is implied for everyone.

---

## 0. Universal capabilities (every authenticated user)

| Use case | Command / mechanism | What it lets them do |
|---|---|---|
| Sign in securely | Auth + MFA | Authenticate; MFA required for all clinical/admin roles |
| See my dashboard | `ANVW` | View a single dashboard that renders only the commands I hold, at my data altitude |
| Use the command bar | UI (⌘K) | Launch any command I hold by typing its mnemonic or searching |
| Receive notifications | Push / SMS | Get alerts relevant to my role (results ready, referrals, low stock, etc.) |
| Act within consent & audit | Consent + audit chain | Every sensitive action I take is checked against patient consent and written to the immutable audit chain |

**Boundaries (everyone):** a request outside my role/geography/tenant/sensitivity scope
returns **403**, ends my session, blacklists the token, and is logged. I only ever see the
slice my four-axis window permits.

---

## 1. Community health

### 1.1 CHW — Binôme
**Mandate:** village-level offline community care (childhood illness, malaria, FP, TB, NCD).
**Bundle:** `CHHH CHIC CHRD CHKT CHFP CHTB CHNC RFNW RFTR PTTM PTVW PBVW`

| Use case | Command | What it lets them do |
|---|---|---|
| See today's visits | `CHHH` | View the household visit list and pending follow-ups |
| Assess a sick child | `CHIC` | Run guided iCCM decision trees (malaria, diarrhoea, pneumonia, malnutrition) |
| Log RDT & dose | `CHRD` | Record rapid-test results; system auto-calculates dose by age/weight |
| Check health kit | `CHKT` | View the virtual health-kit balance per item with low-stock alerts |
| Family planning | `CHFP` | Record contraceptive provision and counselling |
| TB DOT | `CHTB` | Record directly-observed TB treatment |
| NCD prevention | `CHNC` | Record non-communicable-disease prevention activities |
| Refer a severe case | `RFNW` | Create a referral and send a six-digit tracking code to the parent by SMS |
| Track a referral | `RFTR` | Follow the status of a referral they raised |
| Create temp identity | `PTTM` | Register a newborn/unregistered person with a temporary identity |
| View village record | `PTVW` | See the longitudinal record of patients in their assigned village |
| See my PBF score | `PBVW` | View their performance-based-financing score for the period |

**Boundaries:** only their **assigned village** (GPS-polygon enforced, works offline);
cannot see other villages' patients or clinical notes they did not write.

### 1.2 CHW — ASM (maternal & newborn)
**Mandate:** pregnancy and newborn follow-up; facility-delivery promotion.
**Bundle:** `MTAN MTPN CHHH RFNW RFTR PTTM PBVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Antenatal visit | `MTAN` | Register pregnancy; schedule and record antenatal visits and danger signs |
| Postnatal follow-up | `MTPN` | Record postnatal checks of mother and newborn |
| Visit list | `CHHH` | See assigned households and follow-ups |
| Refer / track | `RFNW`, `RFTR` | Refer high-risk cases and track the referral |
| Temp identity | `PTTM` | Create a temporary identity for a newborn |
| PBF score | `PBVW` | View performance score |

**Boundaries:** maternal/newborn scope within their village; no general clinical access.

### 1.3 Cell coordinator
**Mandate:** supervise CHWs; audit kits; validate community data.
**Bundle:** `CHKA CHVD STIN SVAL PBVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Audit kits | `CHKA` | Reconcile physical village health kits against digital records |
| Validate data | `CHVD` | Review and validate community-reported data |
| Stock inquiry | `STIN` | View village/cell stock balances |
| Outbreak alert | `SVAL` | See cell-level disease counts against thresholds |
| PBF | `PBVW` | View cooperative/CHW performance scores |

**Boundaries:** aggregated village data only — **no individual patient clinical records**.

---

## 2. Facility — front desk & clinical

### 2.1 Reception / ADT clerk
**Mandate:** identity, encounter creation, eligibility, co-payment.
**Bundle:** `PTRG PTSR PTVW ENNW CLEL BLVW BLPY APBK APVW APRS`

| Use case | Command | What it lets them do |
|---|---|---|
| Register patient | `PTRG` | Scan national ID, verify via NIDA, auto-fill demographics |
| Search / view patient | `PTSR`, `PTVW` | Find a patient and open their record |
| Open encounter | `ENNW` | Create a new encounter for the visit |
| Check eligibility | `CLEL` | Confirm insurance eligibility at registration |
| Bills & payment | `BLVW`, `BLPY` | View outstanding bills and take a co-payment |
| Appointments | `APBK`,`APVW`,`APRS` | Book, view, and reschedule appointments |

**Boundaries:** no clinical writing (diagnosis, prescriptions); facility-scoped.

### 2.2 OPD clinician / specialist
**Mandate:** consultation, diagnosis, orders, prescriptions.
**Bundle:** `PTSR PTVW ENNW ENHX ENVT ENDX ENNT ENCL RXNW LBOR IMOR RFNW CNVW APBK APVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Review history | `ENHX` | See the patient's longitudinal timeline |
| Record vitals | `ENVT` | Capture/stream vital signs |
| Diagnose | `ENDX` | Record an ICD-10/11 diagnosis (validated against orders) |
| Clinical notes | `ENNT` | Write clinical notes |
| Open / close encounter | `ENNW`, `ENCL` | Manage the encounter lifecycle |
| Prescribe | `RXNW` | Issue a digitally signed prescription; patient gets an SMS code |
| Order labs / imaging | `LBOR`, `IMOR` | Place CPOE lab and imaging orders |
| Refer | `RFNW` | Refer the patient onward with full clinical context |
| View consent | `CNVW` | See the patient's consent settings |
| Appointments | `APBK`,`APVW` | Book and view appointments |

**Boundaries:** only patients **in their care**; cannot see unrelated patients' records.

### 2.3 Emergency physician
**Mandate:** trauma override, critical alerts, pre-hospital review.
**Bundle:** OPD clinician + `PTTM EMTL EMDM`

| Use case | Command | What it lets them do |
|---|---|---|
| (all OPD clinician use cases) | — | Full clinical capability |
| Trauma override identity | `PTTM` | Create a temporary identity for an unidentified critical patient |
| Review pre-hospital telemetry | `EMTL` | See the incoming ambulance's live vitals stream |
| Destination matching | `EMDM` | Confirm the ED as the receiving facility |

**Boundaries:** override actions are heavily audited; temporary identities reconcile to the
permanent record once the patient is stable.

### 2.4 Ward nurse
**Mandate:** medication administration and bedside charting.
**Bundle:** `PTVW ENVT RXVW RXAD`

| Use case | Command | What it lets them do |
|---|---|---|
| View patient | `PTVW` | See assigned-ward patients |
| Record vitals | `ENVT` | Chart bedside vitals |
| View prescriptions | `RXVW` | See the medication schedule |
| Administer medication | `RXAD` | Scan wristband + drug barcode, verify the five rights, record administration |

**Boundaries:** assigned ward only; no financial data; no patients on other wards.

### 2.5 Anaesthetist / theatre team
**Mandate:** perioperative safety and vitals.
**Bundle:** `SXSL SXVT SXRC ENVT`

| Use case | Command | What it lets them do |
|---|---|---|
| Surgical safety checklist | `SXSL` | Step through the WHO checklist on screen |
| Perioperative vitals | `SXVT`, `ENVT` | Stream high-frequency theatre vitals |
| Operative record | `SXRC` | Record the operative note |

**Boundaries:** theatre/perioperative scope.

### 2.6 Laboratory technologist
**Mandate:** sample tracking and result sign-off.
**Bundle:** `LBSP LBRS LBSN LBVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Track specimen | `LBSP` | Track-and-trace a sample from collection to analyser |
| Enter result | `LBRS` | Record analyser results |
| Sign off | `LBSN` | Verify against reference intervals and sign results into the EMR |
| View results | `LBVW` | Review lab results |

**Boundaries:** lab domain; results flow back to the ordering clinician only.

### 2.7 Radiologist
**Mandate:** imaging interpretation and signed reporting.
**Bundle:** `IMVW IMRP IMSN`

| Use case | Command | What it lets them do |
|---|---|---|
| View images | `IMVW` | Review DICOM images in the PACS viewer |
| Draft report | `IMRP` | Write a structured radiology report |
| Sign report | `IMSN` | Apply a cryptographic digital signature to the report |

**Boundaries:** imaging queue; signed report returns to the ordering clinician.

### 2.8 Midwife
**Mandate:** delivery records and birth registration.
**Bundle:** `MTAN MTDL MTBR MTPN PTTM`

| Use case | Command | What it lets them do |
|---|---|---|
| Antenatal | `MTAN` | Record antenatal care |
| Delivery record | `MTDL` | Record the delivery |
| Register birth | `MTBR` | Register the birth (feeds civil registration) |
| Postnatal | `MTPN` | Record postnatal follow-up |
| Temp identity | `PTTM` | Create the newborn's temporary identity |

**Boundaries:** maternity scope.

### 2.9 Mortuary officer
**Mandate:** cause-of-death capture feeding vital statistics.
**Bundle:** `MRDR MRCR`

| Use case | Command | What it lets them do |
|---|---|---|
| Death record | `MRDR` | Record death with an ICD-coded cause |
| Civil-registration feed | `MRCR` | Feed the death into civil registration and mortality statistics |

**Boundaries:** death-record scope only.

---

## 3. Facility — leadership & back office

### 3.1 Health-centre / sector director
**Mandate:** catch village referrals; community performance; PBF payments.
**Bundle:** `RFRC STIN PBSC PBAP CBFB`

| Use case | Command | What it lets them do |
|---|---|---|
| Receive referral | `RFRC` | Open a referred patient by tracking code (full CHW assessment loads) |
| Stock inquiry | `STIN` | Monitor facility stock vs. thresholds |
| Score PBF | `PBSC` | Evaluate CHW cooperative performance |
| Approve PBF payment | `PBAP` | Trigger performance-based payments |
| Fund balance | `CBFB` | View the sector mutuelle/PBF fund position |

**Boundaries:** facility/sector scope; not district-wide or other facilities' records.

### 3.2 Hospital director
**Mandate:** facility-scoped management.
**Bundle:** `STIN CLST HRLC PBSC`

| Use case | Command | What it lets them do |
|---|---|---|
| Stock inquiry | `STIN` | See facility stock and expiry exposure |
| Settlement status | `CLST` | Track insurance receivables/settlement |
| Licence compliance | `HRLC` | Monitor staff licence/compliance status |
| PBF scoring | `PBSC` | View facility PBF performance |
| Dashboard (KPIs) | `ANVW` | Bed occupancy, throughput, revenue, quality, HMIS compliance, with drill-down |

**Boundaries:** their facility tenant only; no individual records outside management need.

### 3.3 Hospital finance
**Bundle:** `CLSB CLST BLVW CBFB`

| Use case | Command | What it lets them do |
|---|---|---|
| Submit claims | `CLSB` | Submit claim batches |
| Settlement status | `CLST` | Track settlement and AR ageing |
| View bills | `BLVW` | Review patient bills |
| Fund balance | `CBFB` | View fund position |

**Boundaries:** financial function within the facility tenant.

### 3.4 Hospital HR
**Bundle:** `HRON HRCT HRTR HRLC HRTN ADUC ADUE`

| Use case | Command | What it lets them do |
|---|---|---|
| Onboard staff | `HRON` | Onboard using NIDA + professional-council licence check |
| Generate contract | `HRCT` | Produce a signed digital contract (Labour Law N° 017/2020) with QR seal |
| Transfer staff | `HRTR` | Move a staff member; old access revoked, new granted automatically |
| Licence tracking | `HRLC` | Track licence expiry; block clinical duties on lapse |
| Training records | `HRTN` | Track mandatory training |
| Create / edit user | `ADUC`, `ADUE` | Provision accounts and set scope |

**Boundaries:** HR within the facility tenant; access provisioning is least-privilege.

### 3.5 Claims officer
**Bundle:** `CLSB CLSC CLRV CLST`

| Use case | Command | What it lets them do |
|---|---|---|
| Submit claims | `CLSB` | Submit claim batches |
| Scrubbing queue | `CLSC` | Work the AI-scrubbed queue |
| Review dispute | `CLRV` | Review AI-flagged disputes |
| Settlement status | `CLST` | Track outcomes |

**Boundaries:** claims function; clinical content limited to what the claim requires.

---

## 4. Pharmacy & supply chain

### 4.1 Dispensing pharmacist
**Bundle:** `RXVF RXDP STIN STEX PHCS CTVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Verify prescription | `RXVF` | Review and confirm a prescription before dispensing |
| Dispense | `RXDP` | Dispense under FEFO with barcode batch/expiry verification |
| Stock inquiry | `STIN` | Check stock levels |
| Expiry monitoring | `STEX` | See items expiring at 90/60/30 days |
| Controlled substances | `PHCS` | Maintain the controlled-substance register |
| View catalogue | `CTVW` | Look up the medicine master catalogue |

**Boundaries:** prescription/stock scope; cannot see other prescriptions beyond what is
being dispensed.

### 4.2 Pharmacy cashier / technician
**Bundle:** `PHPS PHSP PHMM PHEB STIN`

| Use case | Command | What it lets them do |
|---|---|---|
| Point-of-sale | `PHPS` | Ring up a retail/prescription sale |
| Insurer/patient split | `PHSP` | Split the transaction automatically |
| Mobile-money pay | `PHMM` | Initiate MoMo request-to-pay |
| EBM receipt | `PHEB` | Generate the RRA-EBM certified receipt |
| Stock inquiry | `STIN` | Check availability |

**Boundaries:** POS only; no clinical access.

### 4.3 Pharmacy owner
**Bundle:** `STIN STEX CLST SCRO BLVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Stock & expiry | `STIN`, `STEX` | See stock levels and expiry exposure (monetary) |
| Settlement status | `CLST` | Track insurer receivables by payer and age |
| Reorder | `SCRO` | See reorder recommendations from sales velocity |
| View bills | `BLVW` | See sales/receivables — **no patient names** |
| Money dashboard | `ANVW` | Cash, receivables, margins, expiry exposure |

**Boundaries:** financial/inventory view only — **no individual patient records or clinical
detail**.

### 4.4 Procurement officer
**Bundle:** `SCMP SCRO SCPO SCRV STIN STRC`

| Use case | Command | What it lets them do |
|---|---|---|
| B2B marketplace | `SCMP` | Browse verified distributor catalogues |
| Reorder recommendation | `SCRO` | Get optimal reorder quantities from 90-day velocity |
| Purchase order | `SCPO` | Execute a purchase order |
| Goods-receiving verify | `SCRV` | Verify deliveries against the PO |
| Stock inquiry / receive | `STIN`, `STRC` | Monitor stock; receive goods capturing batch/expiry |

**Boundaries:** procurement scope for their facility/pharmacy.

### 4.5 Wholesaler / distributor (seller side)
**Bundle:** `SCCT SCMP PHEB`

| Use case | Command | What it lets them do |
|---|---|---|
| Publish catalogue | `SCCT` | Maintain catalogue, pricing, batch expiry, quantities |
| Marketplace | `SCMP` | Participate in the B2B marketplace |
| EBM invoice | `PHEB` | Issue the certified B2B invoice |

**Boundaries:** their own catalogue and orders; no patient/clinical data.

---

## 5. Patients & citizens

### 5.1 Patient (smartphone)
**Bundle:** `PTVW PTFC RXVW LBVW IMVW BLVW BLPY CNGR CNRV RFTR EMSO APBK APVW APRS`

| Use case | Command | What it lets them do |
|---|---|---|
| View my record | `PTVW` | See my own longitudinal record and care timeline |
| Find care | `PTFC` | Search for care by condition, filter by insurance acceptance and est. co-pay |
| View prescriptions | `RXVW` | See active prescriptions with redemption codes and nearest in-stock pharmacy |
| View results | `LBVW`, `IMVW` | See lab and imaging results |
| Bills & pay | `BLVW`, `BLPY` | See bills (insured/out-of-pocket split) and pay by mobile money |
| Manage consent | `CNGR`, `CNRV` | Grant or revoke consent for specific actors |
| Track referral | `RFTR` | Follow a referral's status |
| Emergency SOS | `EMSO` | One-tap SOS sending GPS to SAMU 912 |
| Appointments | `APBK`,`APVW`,`APRS` | Book, view, reschedule appointments |
| AI first-aid | App | Use the first-aid assistant in Kinyarwanda/French/English |

**Boundaries:** **their own record only** — never any other patient's data.

### 5.2 Patient (feature phone / USSD)
**Bundle:** `RXVW BLPY RFTR` (USSD subset)

| Use case | Command | What it lets them do |
|---|---|---|
| Prescription codes | `RXVW` | Receive prescription redemption codes by SMS |
| Pay | `BLPY` | Pay via USSD/mobile money |
| Track referral | `RFTR` | Check referral status |
| Reminders | SMS | Receive appointment and prescription-ready reminders |

**Boundaries:** USSD/SMS-deliverable subset of the patient capabilities.

### 5.3 Caregiver / proxy
**Bundle:** patient subset, **consent-delegated**

| Use case | Command | What it lets them do |
|---|---|---|
| Manage a dependant | patient subset | Act on behalf of a dependant within the consent the patient/guardian granted |

**Boundaries:** strictly limited to the delegated dependant and granted consent scope.

### 5.4 Diaspora (abroad)
**Bundle:** `BLXB BLVW`

| Use case | Command | What it lets them do |
|---|---|---|
| Cross-border payment | `BLXB` | Pay for a named family member's medicine or bill from abroad |
| View bills | `BLVW` | See the bill for the named dependant (within consent) |

**Boundaries:** payment + named-dependant bill only; no clinical record access.

---

## 6. Emergency & ambulance

### 6.1 Ambulance crew (paramedic / EMT)
**Bundle:** `EMCF EMTL EMDM EMHO EMRT`

| Use case | Command | What it lets them do |
|---|---|---|
| Pre-hospital case file | `EMCF` | Open an emergency case file on scene |
| Telemetry stream | `EMTL` | Stream ECG/BP/SpO₂ to the destination hospital |
| Destination matching | `EMDM` | See the system-selected best receiving facility |
| Handover | `EMHO` | Flow the pre-hospital record into the hospital EMR (no re-keying) |
| Route | `EMRT` | Follow the optimised route on the tablet |

**Boundaries:** the active case; ambulance tablet works offline and reconciles on reconnect.

### 6.2 SAMU 912 dispatch controller
**Bundle:** `EMIN EMDS EMFL EMRT`

| Use case | Command | What it lets them do |
|---|---|---|
| Intake request | `EMIN` | Receive 912 calls, app SOS (GPS), and facility transfer requests |
| Dispatch nearest unit | `EMDS` | Dispatch the closest available ambulance (PostGIS proximity) |
| Fleet management | `EMFL` | Monitor fleet status and allocate across incidents |
| Route to crew | `EMRT` | Push the route to the crew |

**Boundaries:** dispatch/fleet scope; coordinates with receiving facilities on bed
availability.

---

## 7. District & provincial

### 7.1 District Health Officer (DHO)
**Bundle:** `STIN STTR CBFB EMFL PBSC`

| Use case | Command | What it lets them do |
|---|---|---|
| Stock inquiry | `STIN` | See stock/stockout risk across district facilities |
| Inter-facility transfer | `STTR` | Execute stock transfers between facilities |
| Fund balance | `CBFB` | Track the district mutuelle fund |
| Fleet | `EMFL` | See ambulance fleet status in the district |
| PBF scoring | `PBSC` | Review facility performance vs. targets |

**Boundaries:** district-scoped aggregates; not individual clinical records.

### 7.2 District epidemiologist
**Bundle:** `SVMP SVAL SVOR SVDQ STIN`

| Use case | Command | What it lets them do |
|---|---|---|
| Cluster map | `SVMP` | See the real-time ICD-coded disease map by village/sector |
| Outbreak alert | `SVAL` | Monitor notifiable-disease counts vs. thresholds |
| Outbreak response | `SVOR` | Coordinate response from the platform |
| Data quality | `SVDQ` | Track facility reporting completeness/quality |
| Stock inquiry | `STIN` | See stock levels across facilities |

**Boundaries:** counts and clusters — **no patient names or individual notes**.

### 7.3 District pharmacist / stock manager
**Bundle:** `STIN STTR STEX SCNS`

| Use case | Command | What it lets them do |
|---|---|---|
| Stock inquiry | `STIN` | District inventory visibility |
| Transfer | `STTR` | Inter-facility stock transfers |
| Expiry | `STEX` | Monitor expiry exposure |
| Supply intelligence | `SCNS` | See district supply/stockout projection |

**Boundaries:** district inventory scope.

### 7.4 District CBHI / mutuelle manager
**Bundle:** `CBEN CBPR CBPP CBFB CLST`

| Use case | Command | What it lets them do |
|---|---|---|
| Enrolment | `CBEN` | Manage mutuelle enrolment |
| Premiums | `CBPR` | Track premiums/collections |
| Provider payments | `CBPP` | Pay providers |
| Fund balance | `CBFB` | Track the fund as a live balance sheet |
| Settlement | `CLST` | Track claim settlement |

**Boundaries:** financial/enrolment scope; not clinical content of claims.

### 7.5 Provincial coordinator
**Bundle:** `ANVW` (province aggregates)

| Use case | Command | What it lets them do |
|---|---|---|
| Provincial dashboard | `ANVW` | Compare districts; supervise the provincial hospital; support lagging performers |

**Boundaries:** district-level aggregates only; no facility-level individual records.

---

## 8. National government & regulators

### 8.1 MoH / national
**Bundle:** `SVMP SCNS CBFB ITDQ` (de-identified)

| Use case | Command | What it lets them do |
|---|---|---|
| Surveillance map | `SVMP` | National disease surveillance view |
| Supply intelligence | `SCNS` | National stockout risk and RMS distribution status |
| Fund balance | `CBFB` | National CBHI fund position |
| Data quality | `ITDQ` | DHIS2 completeness/timeliness |
| National dashboard | `ANVW` | Population-health, performance, financial, infrastructure indicators |

**Boundaries:** **aggregated and de-identified only** — never an individual patient record.

### 8.2 RBC programme manager
**Bundle:** `SVMP SVAL`

| Use case | Command | What it lets them do |
|---|---|---|
| Programme surveillance | `SVMP`, `SVAL` | Monitor their national programme (HIV/TB/malaria/immunisation) and eIDSR |

**Boundaries:** their programme data; de-identified.

### 8.3 Rwanda FDA
**Bundle:** `RGDR RGLI RGPV RGRC RGLC CTMG`

| Use case | Command | What it lets them do |
|---|---|---|
| Drug registration | `RGDR` | Register drugs |
| Import licence | `RGLI` | Manage import licences |
| Pharmacovigilance | `RGPV` | Track adverse-drug-reaction signals |
| Recall | `RGRC` | Manage recalls and compliance |
| Licence registry | `RGLC` | Maintain practitioner/facility licence registry |
| Manage catalogue | `CTMG` | Maintain the medicine master (FDA reg / ATC / EBM tax) |

**Boundaries:** regulatory scope; **no patient clinical records or financial transactions**.

### 8.4 RSSB (insurer / clearing house)
**Bundle:** `CLSC CLRV CLST CLUT SEAN`

| Use case | Command | What it lets them do |
|---|---|---|
| Scrubbing queue | `CLSC` | Work the AI claims-scrubbing pipeline |
| Review dispute | `CLRV` | Review flagged disputes |
| Settlement | `CLST` | Track settlement time and status |
| Utilisation | `CLUT` | Report utilisation by scheme/provider |
| Fraud signals | `SEAN` | See anomaly/fraud signals |

**Boundaries:** claims pipeline and aggregate utilisation; individual diagnoses only as the
claim requires.

### 8.5 RMS (Rwanda Medical Supply)
**Bundle:** `SCNS STIN CTMG`

| Use case | Command | What it lets them do |
|---|---|---|
| Supply intelligence | `SCNS` | National supply/stockout projection for procurement planning |
| Stock inquiry | `STIN` | National stock visibility |
| Manage catalogue | `CTMG` | Maintain Essential Medicines List entries |

**Boundaries:** supply-chain scope.

### 8.6 National Pharmacy Council
**Bundle:** `RGLC`

| Use case | Command | What it lets them do |
|---|---|---|
| Licence registry | `RGLC` | Maintain pharmacist registration/licence status |

**Boundaries:** pharmacist licensing only.

---

## 9. Humanitarian

### 9.1 Camp clinic medical officer
**Bundle:** OPD clinician (camp tenant)

| Use case | Command | What it lets them do |
|---|---|---|
| (OPD clinician use cases) | — | Full clinical care **within the camp tenant** |

**Boundaries:** camp tenant scope; refugee identity via UNHCR ProGres.

### 9.2 Camp pharmacist
**Bundle:** `RXDP PHPS STIN` (donor ledger, zero patient cost)

| Use case | Command | What it lets them do |
|---|---|---|
| Dispense | `RXDP` | Dispense against the donor grant ledger at zero patient cost |
| POS | `PHPS` | Record the dispense transaction |
| Stock inquiry | `STIN` | Check camp stock |

**Boundaries:** camp tenant; billing against the donor grant, not the patient.

### 9.3 Refugee / displaced patient
**Bundle:** scoped patient access (identity via UNHCR ProGres)

| Use case | Command | What it lets them do |
|---|---|---|
| (scoped patient use cases) | — | Access their own record; donor-subsidised billing |

**Boundaries:** their own record; camp-tenant scope.

---

## 10. External partners

### 10.1 Private hospital / clinic
Acts as its **own tenant** — its staff hold the relevant clinical/pharmacy/leadership bundles
above, scoped to that tenant's data only.

### 10.2 Private insurer
**Bundle:** `CLEL CLRV CLST` (own claims)

| Use case | Command | What it lets them do |
|---|---|---|
| Eligibility | `CLEL` | Check eligibility for their members |
| Review dispute | `CLRV` | Review their own flagged claims |
| Settlement | `CLST` | Track their own settlement |

**Boundaries:** **only their own claims**; no other insurer's or unrelated patient data.

### 10.3 Donor / multilateral
**Bundle:** `DNRP` (anonymised)

| Use case | Command | What it lets them do |
|---|---|---|
| Programme reporting | `DNRP` | View anonymised, aggregated indicators for their funded programme only |

**Boundaries:** read-only, anonymised; no individual records or financial detail beyond
programme-level spend.

### 10.4 Research / academic partner
**Bundle:** `RSRQ RSDS` (governed / anonymised)

| Use case | Command | What it lets them do |
|---|---|---|
| Request data | `RSRQ` | Submit a governed research data request |
| Provision dataset | `RSDS` | Receive a governed, anonymised, consent-bound dataset |

**Boundaries:** anonymised and consent-bound; governed by approval.

---

## 11. Platform administration

### 11.1 IT / SOC analyst
**Bundle:** `SESD SELK SEWA SEAN SEKR SEPT ADAU ITSY ITBK ITSN ITIN ITDQ ITEP`

| Use case | Command | What it lets them do |
|---|---|---|
| Security dashboard | `SESD` | Monitor security posture 24/7 |
| LOCK | `SELK` | Kill a session, blacklist its JWT, lock the account |
| WAF rules | `SEWA` | Manage web-application-firewall rules |
| Anomaly / fraud | `SEAN` | Triage anomaly and fraud alerts |
| Key management | `SEKR` | Rotate and custody encryption keys (HSM/Vault) |
| Pen-test / vuln | `SEPT` | Manage penetration tests and remediation |
| Audit-chain view | `ADAU` | Inspect the immutable audit chain |
| SysOps health | `ITSY` | Monitor cluster/container/connection health |
| Backup / restore | `ITBK` | Manage backups and restore tests |
| Offline-sync | `ITSN` | Manage the offline-sync layer |
| Integration endpoints | `ITIN` | Monitor NIDA/EBM/FHIR integrations and retries |
| Data quality | `ITDQ` | Monitor completeness/timeliness |
| Endpoint / device | `ITEP` | Manage terminals, tablets, and CHW phones |

**Boundaries:** security/infrastructure scope — **no clinical content of patient records**.

### 11.2 Super-admin (DG of Digitisation)
**Bundle:** all `AD*` + `SE*` + `IT*`

| Use case | Command | What it lets them do |
|---|---|---|
| User lifecycle | `ADUC ADUE ADUR` | Create, edit/scope, revoke/deactivate users |
| Assign commands | `ADCA`, `ADCB` | Assign commands and manage command bundles |
| Audit-chain view | `ADAU` | Inspect the audit chain |
| (all SOC + IT use cases) | `SE* IT*` | Full security and IT operations |

**Boundaries:** the highest-trust role — every action is itself audited; provisioning others
follows least privilege.

---

## Cross-references
- Commands & bundles: [03 — Command Catalogue](03-command-catalogue.md)
- Access model: [04 — Access-Control Model](04-access-control-model.md)
- What each role may/may not **see**: [13 — Data Visibility by Role](13-data-visibility-by-role.md)
- Formal use-case model (diagram + flows): [53 — Use Case Model](53-use-case-model.md)
- Requirement traceability: [62 — Requirements Traceability Matrix](62-requirements-traceability-matrix.md)

> **Note on completeness:** this catalogue reflects the command bundles in doc 03. As bundles
> are tuned per deployment (an admin adds/removes individual commands), a specific user's real
> capability set is always *exactly the commands assigned to them* — this document describes
> the standard preset for each role.
