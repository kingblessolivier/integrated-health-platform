# 25 — Load Balancing & Performance

## Load-balancing architecture

- **Layer 4 (TCP):** a load balancer distributes incoming connections across NGINX
  reverse-proxy nodes.
- **Layer 7 (HTTP):** HAProxy distributes application requests across backend containers
  using the **Least-Connections** algorithm.
- **Health checks:** HAProxy pings each backend every 2 seconds; unhealthy backends are
  removed from the pool within 4 seconds.

## Horizontal scaling

- Django application containers are **stateless**; Kubernetes scales them horizontally on CPU
  utilisation (target **60%**).
- During end-of-month insurance-settlement surges, the application tier scales out
  automatically within **60 seconds**.
- Reporting and analytics queries are routed to PostgreSQL **read replicas**, keeping write
  traffic on the primary.

## Caching strategy

- **Redis** caches: session tokens, rate-limit counters, JWT blacklist, materialised
  dashboard data, drug catalogue, ICD codes, and geographic boundaries.
- Static assets are served from the **Cloudflare CDN** edge.
- Expensive aggregate query results are cached in Redis with a **TTL aligned to the data's
  update frequency**.

## Performance targets

| Operation | Target |
|---|---|
| Patient registration (NIDA handshake → encounter creation) | < 2 s at the 95th percentile |
| Prescription-code lookup at the pharmacy counter | < 500 ms |
| Dashboard load (materialised view) | < 1 s |
| EBM invoice transmission (payment confirmation → receipt print) | < 3 s |
| FHIR bundle push to DHIS2 (hourly batch) | < 30 s |
| Database failover (primary promotion) | < 10 s |
