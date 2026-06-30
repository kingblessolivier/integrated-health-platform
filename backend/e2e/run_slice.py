"""
Data-layer end-to-end harness for the Clinical Slice.

Seeds a minimal dataset and walks the whole flow against a REAL Postgres (the schema from
backend/sql/0001_initial.sql), exercising the actual business-logic services:
register patient -> encounter -> diagnosis -> prescription -> FEFO dispense -> POS checkout
-> claim scrub/advance. Asserts the important invariants (FEFO picks the earliest in-date
batch, stock decrements, payment split sums to total, claim reaches 'approved').

This bypasses the HTTP/JWT layer on purpose (auth bootstrapping is a separate task — see
docs/65). It proves the schema + models + services agree against a live database.

Run (with the compose db up and schema applied):
    cd backend && python -m e2e.run_slice
Env: DATABASE_URL, or POSTGRES_{HOST,PORT,DB,USER,PASSWORD}.
"""
import os
import sys
from collections import namedtuple
from datetime import date, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg  # noqa: E402

from apps.billing.services import issue_ebm_receipt, split_payment  # noqa: E402
from apps.claims.services import advance, scrub  # noqa: E402
from apps.pharmacy.services import select_fefo  # noqa: E402

Batch = namedtuple("Batch", "id batch expiry_date quantity")


def _conninfo() -> str:
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    parts = [
        f"host={os.environ.get('POSTGRES_HOST', 'localhost')}",
        f"port={os.environ.get('POSTGRES_PORT', '5432')}",
        f"dbname={os.environ.get('POSTGRES_DB', 'inhp')}",
        f"user={os.environ.get('POSTGRES_USER', 'inhp')}",
    ]
    password = os.environ.get("POSTGRES_PASSWORD")  # from .env locally; CI uses trust auth
    if password:
        parts.append(f"password={password}")
    return " ".join(parts)


def _one(cur, sql, params=()):
    cur.execute(sql, params)
    return cur.fetchone()[0]


def run(conn):
    cur = conn.cursor()
    today = date.today()

    # --- seed -------------------------------------------------------------
    tenant = _one(cur, "INSERT INTO tenants(name, kind) VALUES (%s,'facility') RETURNING id",
                  ("Demo District Hospital",))
    insurer = _one(cur, "INSERT INTO tenants(name, kind) VALUES (%s,'insurer') RETURNING id",
                   ("RSSB",))
    cur.execute("SELECT set_config('app.tenant_id', %s, false)", (str(tenant),))
    facility = _one(cur, "INSERT INTO facilities(tenant_id, name, level) "
                         "VALUES (%s,%s,'health_centre') RETURNING id", (tenant, "Demo HC"))
    staff = _one(cur, "INSERT INTO staff(tenant_id, facility_id, full_name) "
                      "VALUES (%s,%s,%s) RETURNING id", (tenant, facility, "Dr. Demo"))
    product = _one(cur, "INSERT INTO products(name, atc) VALUES (%s,%s) RETURNING id",
                   ("Artemether-Lumefantrine", "P01BF01"))
    patient = _one(cur, "INSERT INTO patients(tenant_id, given_name, family_name, sex) "
                        "VALUES (%s,%s,%s,'female') RETURNING id", (tenant, "Aline", "U."))

    # two batches: one near expiry (should win under FEFO), one later
    _one(cur, "INSERT INTO stock_items(tenant_id, facility_id, product_id, batch, expiry_date, "
              "quantity) VALUES (%s,%s,%s,'LATE',%s,100) RETURNING id",
         (tenant, facility, product, today + timedelta(days=120)))
    _one(cur, "INSERT INTO stock_items(tenant_id, facility_id, product_id, batch, expiry_date, "
              "quantity) VALUES (%s,%s,%s,'SOON',%s,100) RETURNING id",
         (tenant, facility, product, today + timedelta(days=20)))

    # --- clinical ---------------------------------------------------------
    encounter = _one(cur, "INSERT INTO encounters(tenant_id, facility_id, patient_id, status, "
                          "created_by) VALUES (%s,%s,%s,'open',%s) RETURNING id",
                     (tenant, facility, patient, staff))
    _one(cur, "INSERT INTO diagnoses(tenant_id, encounter_id, icd_code, created_by) "
              "VALUES (%s,%s,'B54',%s) RETURNING id", (tenant, encounter, staff))
    rx = _one(cur, "INSERT INTO prescriptions(tenant_id, encounter_id, code, status, signed_by, "
                   "signature) VALUES (%s,%s,'RX123','signed',%s,%s) RETURNING id",
              (tenant, encounter, staff, b""))
    _one(cur, "INSERT INTO prescription_items(tenant_id, prescription_id, product_id, quantity) "
              "VALUES (%s,%s,%s,24) RETURNING id", (tenant, rx, product))

    # --- FEFO dispense ----------------------------------------------------
    cur.execute("SELECT id, batch, expiry_date, quantity FROM stock_items "
                "WHERE facility_id=%s AND product_id=%s", (facility, product))
    batches = [Batch(*row) for row in cur.fetchall()]
    chosen = select_fefo(batches, today=today)
    assert chosen is not None and chosen.batch == "SOON", f"FEFO picked {chosen}"

    qty = 24
    cur.execute("UPDATE stock_items SET quantity = quantity - %s WHERE id=%s",
                (qty, chosen.id))
    dispense = _one(cur, "INSERT INTO dispenses(tenant_id, stock_item_id, quantity, "
                         "dispensed_by) VALUES (%s,%s,%s,%s) RETURNING id",
                    (tenant, chosen.id, qty, staff))
    _one(cur, "INSERT INTO stock_movements(tenant_id, stock_item_id, kind, quantity, ref_id, "
              "created_by) VALUES (%s,%s,'dispense',%s,%s,%s) RETURNING id",
         (tenant, chosen.id, -qty, dispense, staff))
    remaining = _one(cur, "SELECT quantity FROM stock_items WHERE id=%s", (chosen.id,))
    assert remaining == 100 - qty, f"stock not decremented: {remaining}"

    # --- POS checkout -----------------------------------------------------
    total = Decimal("5000")
    insurer_portion, out_of_pocket = split_payment(total, 0.9)
    assert insurer_portion + out_of_pocket == total
    txn = _one(cur, "INSERT INTO transactions(tenant_id, facility_id, patient_id, "
                    "insurer_portion, out_of_pocket, ebm_token) VALUES (%s,%s,%s,%s,%s,%s) "
                    "RETURNING id",
               (tenant, facility, patient, insurer_portion, out_of_pocket, issue_ebm_receipt()))
    _one(cur, "INSERT INTO payments(tenant_id, transaction_id, method, status, amount) "
              "VALUES (%s,%s,'momo','pending',%s) RETURNING id", (tenant, txn, out_of_pocket))
    claim = _one(cur, "INSERT INTO claims(tenant_id, transaction_id, insurer_id, status, amount) "
                      "VALUES (%s,%s,%s,'submitted',%s) RETURNING id",
                 (tenant, txn, insurer, insurer_portion))

    # --- claim scrub + advance -------------------------------------------
    passed, reason = scrub(insurer_portion, has_diagnosis=True, billed_matches=True)
    assert passed and reason is None
    status = advance(advance("submitted", "scrub_start"), "scrub_pass")
    assert status == "approved"
    cur.execute("UPDATE claims SET status=%s WHERE id=%s", (status, claim))

    conn.commit()
    print("E2E PASS: register -> encounter -> diagnosis -> Rx -> FEFO dispense "
          f"(batch {chosen.batch}, {remaining} left) -> checkout "
          f"(insurer {insurer_portion} / oop {out_of_pocket}) -> claim {status}")


def main():
    with psycopg.connect(_conninfo()) as conn:
        try:
            run(conn)
        except AssertionError as exc:
            print(f"E2E FAIL: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
