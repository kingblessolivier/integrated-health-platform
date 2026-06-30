"""
Pure Performance-Based Financing logic (no DB) — unit-tested in tests.py (docs/20).
Scores CHW cooperatives / facilities on weighted indicators (0..1) and computes the payment.
"""


def compute_pbf_score(metrics: dict, weights: dict | None = None) -> float:
    """Weighted score on a 0–100 scale from indicator values in [0, 1]."""
    if not metrics:
        return 0.0
    weights = weights or {k: 1 for k in metrics}
    total_weight = sum(weights.get(k, 0) for k in metrics)
    if total_weight == 0:
        return 0.0
    weighted = sum(metrics[k] * weights.get(k, 0) for k in metrics)
    return round(weighted / total_weight * 100, 1)


def payment_for_score(score: float, max_amount) -> float:
    """Proportional payment: a 0–100 score scales the maximum reward."""
    score = max(0.0, min(100.0, float(score)))
    return round(float(max_amount) * score / 100, 2)
