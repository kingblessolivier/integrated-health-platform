"""
Append-only, SHA-256-chained audit log (see docs/34 and docs/48).

current_hash = SHA256(prev_hash || payload_hash || actor_id || ts)
Any later edit to a historical row breaks every subsequent hash and is detected on the
scheduled verification pass.
"""
import hashlib
import json

from django.db import connection


def _sha256(*parts: str) -> str:
    return hashlib.sha256("".join(parts).encode()).hexdigest()


def append(actor_id: str, command: str, resource_type: str, resource_id, payload: dict,
           tenant_id: str | None = None) -> str:
    payload_hash = _sha256(json.dumps(payload, sort_keys=True, default=str))
    with connection.cursor() as cur:
        cur.execute("SELECT current_hash FROM audit_log ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        prev_hash = row[0] if row else "GENESIS"
        cur.execute("SELECT now()::text")
        ts = cur.fetchone()[0]
        current_hash = _sha256(prev_hash, payload_hash, str(actor_id), ts)
        cur.execute(
            """INSERT INTO audit_log
               (tenant_id, actor_id, command, resource_type, resource_id,
                payload_hash, prev_hash, current_hash, ts)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            [tenant_id, actor_id, command, resource_type, resource_id,
             payload_hash, prev_hash, current_hash, ts],
        )
    return current_hash
