from apps.surveillance.services import aggregate_counts, detect_outbreaks


def test_aggregate_counts_groups_by_key():
    cases = [{"disease": "B54"}, {"disease": "B54"}, {"disease": "J18.9"}]
    assert aggregate_counts(cases) == {"B54": 2, "J18.9": 1}


def test_detect_outbreaks_default_threshold():
    alerts = detect_outbreaks({"B54": 12, "J18.9": 3}, default_threshold=10)
    assert alerts == [{"key": "B54", "count": 12, "threshold": 10}]


def test_detect_outbreaks_per_key_threshold():
    alerts = detect_outbreaks({"B54": 5, "A09": 2}, thresholds={"A09": 2}, default_threshold=10)
    assert alerts == [{"key": "A09", "count": 2, "threshold": 2}]


def test_detect_outbreaks_sorted_by_count_desc():
    alerts = detect_outbreaks({"X": 20, "Y": 50, "Z": 30}, default_threshold=1)
    assert [a["key"] for a in alerts] == ["Y", "Z", "X"]


def test_detect_outbreaks_none_threshold_flags_nothing():
    assert detect_outbreaks({"B54": 100}) == []
