# 14 — Analytics & Dashboards

Every actor's dashboard shows information at the **exact altitude and scope** their role
requires. The dashboard itself is one command-driven surface (see
[06 — Unified Dashboard](06-unified-dashboard.md)); this doc catalogues *what* each actor
sees. Dashboards are real-time where data permits; otherwise pre-computed on schedule.

## CHW mobile dashboard
- Today's household visit list and pending follow-ups.
- Virtual health-kit balance per item with low-stock alert.
- Open referrals and their tracking-code status.
- Personal PBF score for the current period.

## Cell coordinator
- Village-by-village health-kit balance grid.
- CHW reporting completeness and anomaly flags.
- Cell-wide disease case count for the current week.
- Pending replenishment requests awaiting approval.

## Health centre / sector director
- Daily patient throughput and current queue length.
- Referral in-flow from villages with tracking-code status.
- Facility stock levels against minimum thresholds.
- CHW cooperative PBF scores and payment status.
- Monthly indicator comparison against targets.

## District epidemiologist
- Live ICD-coded diagnosis map across the district by village.
- Notifiable-disease counts against outbreak thresholds with alert status.
- Waterborne, respiratory, and vector-borne trend lines.
- Cluster alert map with drill-down to *umudugudu* level.
- Facility reporting completeness and data-quality score.

## District Health Officer
- Facility performance league table against district targets.
- Stock levels and stockout risk across all facilities.
- Inter-facility transfer recommendations.
- Mutuelle fund: enrolment rate, collections, claims paid, balance.
- Ambulance fleet status within the district.

## Hospital director / leadership
- Live bed occupancy and average length of stay.
- Daily revenue, cash position, and insurance receivables aged by insurer.
- Patient throughput by department.
- Medication-error and incident count.
- Staff on duty vs. required coverage.
- Top 10 diagnoses and top 10 drugs dispensed this week.
- Expiry exposure in monetary value.
- HMIS reporting-compliance status.

## Department heads
- **OPD:** today's appointments, queue status, clinician workload, pending orders.
- **Lab:** specimen backlog, turnaround time, reagent stock.
- **Radiology:** imaging queue, modality utilisation, reports pending sign-off.
- **Pharmacy:** stock alerts, prescription queue, dispensing volume, controlled-substance register.
- **Finance:** daily revenue, AR ageing by insurer, claim-denial reasons.
- **HR:** roster coverage, attendance, licence-expiry alerts.
- **Stores:** stock levels, purchase orders in transit, cold-chain status.

## Pharmacy owner
- Today's sales total and payment-method split (cash / MoMo / insurance).
- Outstanding insurer receivables per payer, aged (30 / 60 / 90+ days).
- Products expiring within 30, 60, 90 days and their stock value.
- Gross margin by product and category.
- Best-selling and slowest-moving products over 90 days.
- Reorder recommendations based on sales velocity.

## Patient portal
- Next appointment with time, doctor, and facility.
- Active prescriptions with redemption codes and the nearest in-stock pharmacy.
- Pending lab and imaging results.
- Outstanding balance with insurance-covered / out-of-pocket split.
- Care-history timeline.
- Consent-management panel.

## National / MoH
- Population health: birth rate, mortality, under-5 and maternal mortality, immunisation coverage.
- Disease surveillance: notifiable counts nationally, province comparison, active outbreak alerts.
- Health-system performance: reporting completeness, bed occupancy, average claims-payment time.
- Supply intelligence: national stockout risk by essential medicine, RMS distribution status.
- Financial: national CBHI fund balance, claims settled vs. pending, average payment lag.
- Infrastructure: API transaction velocity, uptime, node connectivity across rural facilities.
- Data quality: DHIS2 completeness and timeliness scores.

## Rwanda FDA
- Drug-registration status by product and importer.
- Adverse-drug-reaction reports by product and region.
- Active recall status and facility compliance.
- Pharmacovigilance signals — unexpected adverse-event clusters.
- Licence-expiry watch list for facilities and practitioners.

## RSSB / insurance
- Claims pipeline: submitted, scrubbing, approved, paid, rejected — by provider and facility.
- AI-flagged dispute queue with reason codes.
- Average settlement time by insurer and facility type.
- Utilisation rate by scheme (mutuelle, RAMA, private).
- Fraud-signal trends from the anomaly-detection engine.
