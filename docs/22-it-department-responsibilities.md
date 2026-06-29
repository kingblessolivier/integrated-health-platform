# 22 — IT Department Responsibilities

## Systems operations (SysOps / SRE)

- Monitor container health, connection pools, and cache performance.
- Manage Kubernetes cluster scaling; execute and verify database failover drills.
- Maintain backup schedules: **hourly incremental, daily full**, verified with restore tests.
- Manage the **offline-sync layer** for rural and field nodes.

## Security operations (SOC)

- Monitor the security dashboard 24/7; manage WAF rules.
- Execute the **`LOCK`** command on compromised accounts; manage the JWT blacklist.
- Maintain the **immutable audit chain**; verify integrity on schedule.
- Conduct and manage penetration tests and vulnerability remediation.
- Manage encryption keys: rotation schedule, custody, HSM maintenance.

## Helpdesk & endpoint management

- Provision and deprovision user accounts as directed by HR.
- Manage physical terminals at facilities: OS patches, anti-virus, encryption status.
- Manage the device-management system for ambulance tablets and CHW phones.
- Track patch-compliance status of every endpoint across all facilities.

## Data & integration management

- Maintain **HL7 FHIR adapters** to DHIS2 and eIDSR; validate bundle-schema compliance.
- Monitor **NIDA, KWIVUZA, and RRA EBM** integration endpoints; handle failures and retries.
- Monitor data quality: completeness, timeliness, and accuracy at every facility.
- Support research data requests: provision governed, anonymised datasets.
