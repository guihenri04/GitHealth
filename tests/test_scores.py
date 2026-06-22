from __future__ import annotations

from githealth.analysis.durations import build_all_metrics
from githealth.analysis.scores import apply_scores, percentile_ranks


def test_percentile_ranks_handles_ties() -> None:
    assert percentile_ranks([10, 10, 30]) == [33.33, 33.33, 83.33]


def test_apply_scores_sets_size_and_effort_indexes(sample_prs) -> None:
    metrics = apply_scores(build_all_metrics(sample_prs))
    assert metrics[1].change_size_index > metrics[0].change_size_index
    assert metrics[1].review_effort_index > metrics[0].review_effort_index
