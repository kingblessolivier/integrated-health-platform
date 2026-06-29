# 19 — Ambulance & Emergency Management

## Emergency-request intake

- Requests arrive via the **912 hotline**, a one-tap patient-app **SOS** (GPS auto-sent), or
  a **facility transfer** request.
- The SOS GPS transmission eliminates the documented problem of locating patients in rural
  areas with no street addresses.

## Dispatch & routing

- A **PostGIS spatial query** runs over live GPS geohashes from all ambulances to find the
  nearest available unit.
- An assignment with an optimised route is pushed to the crew's vehicle tablet.

## Pre-hospital care & telemetry

- The crew opens an emergency case file; a portable vitals monitor streams **ECG, blood
  pressure, and SpO₂** continuously.
- Clinical findings are recorded; the system packages vitals and findings and transmits them
  to the target hospital.
- The receiving emergency bay sees the pre-hospital data **before the vehicle arrives** and
  prepares the resuscitation room.

## Destination matching

- The system selects the best receiving facility by **open bed, clinical capability, and
  acceptance of the patient's insurance**.
- The facility is pre-alerted and confirms acceptance.

## Handover & record continuity

- At arrival, the pre-hospital record flows directly into the hospital EMR — **no re-keying**.
- For trauma-override cases, the temporary identity is linked to the permanent record when
  the patient is stable.

## Fleet management

- Every ambulance is a tracked asset: live status, location, and type (basic vs. advanced
  life support).
- Maintenance schedules and fuel logs are maintained per vehicle.
- Fleet utilisation, response time, and coverage-gap analysis appear on district and
  national dashboards.
