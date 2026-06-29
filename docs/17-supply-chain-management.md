# 17 — Supply Chain Management

## Supply-chain hierarchy

```
International manufacturers
  → Rwanda FDA & customs clearance
    → Licensed importers / wholesalers (SOPHAR, Ubipharm, Abacus + ~20–30 active importers)
      → Retail pharmacies & private facilities
```

The platform serves the **private channel** and integrates with **RMS** data for national
supply intelligence.

## B2B wholesale marketplace

- Verified distributors publish live catalogues, batch expiry dates, unit prices, and
  available quantities.
- The system analyses **90-day sales velocity** and computes the optimal reorder quantity,
  **drafting the purchase order automatically**.
- The distributor receives a structured digital invoice; fulfilment status is tracked.
- **EBM 2.0 rails** handle the B2B invoice — the purchase auto-loads into the buyer's records.

## Goods receiving

- The storekeeper scans the shipping-manifest barcode and verifies it against the open
  purchase order.
- Each item is scanned to capture **batch, lot, and expiry**; a FEFO index is assigned
  immediately.
- Discrepancies between order and delivery are flagged for supplier resolution.

## National supply intelligence

- Real-time stock visibility across every registered facility enables **early stockout
  projection**.
- Data is shared with **RMS** for national procurement planning and with **MoH** for supply-
  chain policy.
- During import disruptions, the system shows where **buffer stock** exists and suggests
  redistribution.
