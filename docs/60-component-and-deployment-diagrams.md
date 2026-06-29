# 60 — Component & Deployment Diagrams

The static implementation view (components and their interfaces) and the physical view
(how components map to infrastructure). Aligns with the technology stack in
[07](07-technology-stack.md) and deployment doc [23](23-deployment-and-infrastructure.md).

## Component diagram

```mermaid
flowchart TB
    subgraph Clients
      Web[React SPA]
      Mobile[Flutter apps]
      USSD[SMS / USSD]
    end

    GW[API Gateway<br/>rate limit · JWT]

    subgraph Services
      Auth[Auth & Access<br/>4-axis + commands]
      Clinical[Clinical / Encounter]
      Pharmacy[Pharmacy & Inventory]
      Billing[Billing & Claims]
      Emergency[Emergency / Dispatch]
      Analytics[Analytics / Dashboards]
      Integration[Integration adapters]
      Audit[Audit chain]
    end

    subgraph Data
      PG[(PostgreSQL + PostGIS)]
      TS[(TimescaleDB)]
      Redis[(Redis)]
      Mino[(MinIO / DICOM)]
      ES[(Elasticsearch)]
    end

    subgraph External
      NIDA[[NIDA]]
      RSSB[[RSSB/KWIVUZA]]
      EBM[[RRA EBM]]
      HMIS[[DHIS2/eIDSR]]
      SAMU[[SAMU]]
      MoMo[[Mobile Money]]
      AT[[Africa's Talking]]
    end

    Web --> GW
    Mobile --> GW
    USSD --> AT --> GW
    GW --> Auth & Clinical & Pharmacy & Billing & Emergency & Analytics
    Clinical --> PG
    Pharmacy --> PG
    Billing --> PG
    Analytics --> PG
    Clinical --> TS
    Auth --> Redis
    Clinical --> Mino
    Analytics --> ES
    Clinical & Pharmacy & Billing & Emergency --> Audit --> PG
    Integration --> NIDA & RSSB & EBM & HMIS & SAMU & MoMo
    Auth --> Integration
    Billing --> Integration
```

## Deployment diagram

```mermaid
flowchart TB
    subgraph Edge
      CF[Cloudflare WAF / CDN / DDoS]
    end
    subgraph DC["Data centre — within Rwanda"]
      LB[NGINX + HAProxy]
      subgraph K8s[Kubernetes cluster]
        N1[App pods x N<br/>Django/FastAPI]
        N2[Worker pods<br/>Celery]
        N3[Channels/gRPC<br/>streaming]
      end
      subgraph DataTier
        PGp[(PostgreSQL primary<br/>Patroni)]
        PGs[(2x hot standby)]
        Rd[(Redis sentinel)]
        TSn[(TimescaleDB)]
        Obj[(MinIO)]
      end
    end
    subgraph DR["DR site — separate region, Rwanda"]
      Hot[(Hot standby<br/>continuous replication)]
    end
    subgraph Field
      Tab[Ambulance tablet]
      Phone[CHW / patient phone]
    end

    CF --> LB --> K8s
    N1 --> PGp
    PGp --> PGs
    N1 --> Rd
    N3 --> TSn
    N1 --> Obj
    PGp -. WAL replicate .-> Hot
    Tab -. offline sync .-> CF
    Phone -. offline sync .-> CF
```

## Notes
- **Stateless app tier** scales horizontally; **Patroni** manages PostgreSQL HA (failover
  < 10 s); **Redis sentinel** for cache/session HA.
- **Data residency:** all PHI and backups stay within Rwanda; DR is a separate in-country region.
- **Service mesh (Istio)** provides mTLS between services (not drawn, see doc 07/08).
- Field devices reconcile through the edge using the offline op-log (doc 51).
