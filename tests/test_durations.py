from __future__ import annotations

from githealth.analysis.durations import build_pull_request_metrics


def test_calculates_first_review_time(sample_prs) -> None:
    metric = build_pull_request_metrics(sample_prs[0])
    assert metric.first_review_hours == 1
    assert metric.cycle_hours == 4
    assert metric.post_review_hours == 3


def test_counts_commits_after_first_review(sample_prs) -> None:
    metric = build_pull_request_metrics(sample_prs[1])
    assert metric.commits_after_first_review == 2


def test_handles_pull_request_without_review(sample_prs) -> None:
    pr = sample_prs[0]
    without_reviews = pr.__class__(**{**pr.__dict__, "reviews": ()})
    metric = build_pull_request_metrics(without_reviews)
    assert metric.first_review_hours is None
    assert metric.post_review_hours is None
