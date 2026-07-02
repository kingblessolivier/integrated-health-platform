"""
Pure HR/payroll logic (no DB) — unit-tested in tests.py. Monthly PAYE (RRA brackets) + RSSB
pension deductions and licence-expiry tracking (docs/18).

PAYE monthly bands (RWF): 0–60,000 @ 0% · 60,001–100,000 @ 10% · 100,001–200,000 @ 20% ·
>200,000 @ 30%. RSSB employee pension @ 3%. (Confirm current statutory rates before go-live.)
"""
_PAYE_BANDS = [(0, 60000, 0.0), (60000, 100000, 0.10),
               (100000, 200000, 0.20), (200000, float("inf"), 0.30)]


def compute_paye(gross) -> float:
    g = float(gross)
    tax = 0.0
    for low, high, rate in _PAYE_BANDS:
        if g > low:
            tax += (min(g, high) - low) * rate
    return round(tax, 2)


def compute_rssb(gross, rate=0.03) -> float:
    return round(float(gross) * rate, 2)


def net_pay(gross) -> float:
    return round(float(gross) - compute_paye(gross) - compute_rssb(gross), 2)


def licence_status(expires_on, today) -> str:
    """expired | 30 | 60 | 90 | ok — drives the licence-expiry alerts (docs/18)."""
    days = (expires_on - today).days
    if days < 0:
        return "expired"
    if days <= 30:
        return "30"
    if days <= 60:
        return "60"
    if days <= 90:
        return "90"
    return "ok"
