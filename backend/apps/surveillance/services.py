"""
Pure surveillance/analytics logic (no DB) — unit-tested in tests.py. Aggregates de-identified
case counts and flags outbreaks against thresholds (docs/12, docs/14). All outputs are counts,
never individual records — altitude rises, identifiability drops.
"""
from collections import Counter


def aggregate_counts(cases, key="disease") -> dict:
    """Count cases grouped by `key` (e.g. 'disease' or 'location')."""
    counter = Counter()
    for case in cases:
        counter[case.get(key)] += 1
    return dict(counter)


def detect_outbreaks(counts: dict, thresholds: dict | None = None, default_threshold=None):
    """Return [{key, count, threshold}] for every group whose count meets/exceeds its
    threshold (per-key in `thresholds`, else `default_threshold`). Sorted by count desc."""
    thresholds = thresholds or {}
    alerts = []
    for key, count in counts.items():
        threshold = thresholds.get(key, default_threshold)
        if threshold is not None and count >= threshold:
            alerts.append({"key": key, "count": count, "threshold": threshold})
    return sorted(alerts, key=lambda a: a["count"], reverse=True)
