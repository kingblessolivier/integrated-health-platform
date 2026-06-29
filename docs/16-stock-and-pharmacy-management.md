# 16 — Stock & Pharmacy Management

## Product catalogue

- A **master medicine catalogue** covers every registered drug, OTC product, medical device,
  and consumable.
- Each item is tagged with its **Rwanda FDA registration**, **tax category** for EBM, and
  **WHO ATC code**.
- The catalogue is shared across all facilities — a drug means the same thing everywhere.

## Inventory & FEFO enforcement

- Every stock item is tracked by **batch number, lot, quantity, expiry date, and shelf
  location**.
- **First-Expiring, First-Out (FEFO)** is enforced at dispensing: the system always selects
  the batch closest to expiry.
- **Low-stock alerts** fire when stock falls below a configurable safety threshold.
- **Expiry alerts** fire at 90, 60, and 30 days; the monetary value at risk is quantified.
- A **stock-take module** reconciles physical counts against digital records.

## Point-of-sale counter

- Walk-in retail sales and prescription fulfilments write to the **same inventory and the
  same ledger**.
- Barcode scanning verifies product identity; the system rejects items not in the registered
  catalogue.
- Transactions are split between **insurer and out-of-pocket** portions automatically.
- **Mobile-money request-to-pay** is initiated within the POS; confirmation triggers receipt
  generation.
- An **RRA EBM certified invoice** is generated and transmitted in real time on every
  completed transaction.

## Cold-chain management

- IoT temperature sensors log readings **every 60 seconds** inside vaccine and cold-chain
  storage.
- If temperature drifts outside **2 °C – 8 °C**, a critical alert fires to IT and facility
  management.
- Temperature logs are retained as compliance records.
