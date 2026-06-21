from __future__ import annotations

from githealth.analysis.durations import build_pull_request_metrics


def test_calculates_first_review_time(sample_prs) -> None:
    metric = build_pull_request_metrics(sample_prs[0])
    assert metric.first_review_hours == 1
    assert metric.cycle_hours == 4
    assert metric.post_review_hours == 3
