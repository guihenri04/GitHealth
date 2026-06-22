from __future__ import annotations

import math
from collections.abc import Callable

from githealth.models import PullRequestMetrics


def percentile_ranks(values: list[float]) -> list[float]:
    if not values:
        return []
    if len(values) == 1:
        return [100.0]

    sorted_values = sorted(values)
    ranks: list[float] = []
    for value in values:
        less = sum(1 for item in sorted_values if item < value)
        equal = sum(1 for item in sorted_values if item == value)
        rank = (less + 0.5 * equal) / len(sorted_values) * 100
        ranks.append(round(rank, 2))
    return ranks


def _score(
    metrics: list[PullRequestMetrics],
    extractors: list[Callable[[PullRequestMetrics], float]],
) -> list[float]:
    columns = [[extractor(metric) for metric in metrics] for extractor in extractors]
    ranked_columns = [percentile_ranks(column) for column in columns]
    scores: list[float] = []
    for index in range(len(metrics)):
        score = sum(column[index] for column in ranked_columns) / len(ranked_columns)
        scores.append(round(score, 2))
    return scores


def apply_scores(metrics: list[PullRequestMetrics]) -> list[PullRequestMetrics]:
    size_scores = _score(
        metrics,
        [
            lambda metric: math.log1p(metric.churn),
            lambda metric: float(metric.changed_files),
            lambda metric: float(metric.commits),
        ],
    )
    effort_scores = _score(
        metrics,
        [
            lambda metric: float(metric.review_comments),
            lambda metric: float(metric.number_of_reviews),
            lambda metric: float(metric.changes_requested),
            lambda metric: float(metric.commits_after_first_review),
        ],
    )
    for metric, size_score, effort_score in zip(metrics, size_scores, effort_scores, strict=True):
        metric.change_size_index = size_score
        metric.review_effort_index = effort_score
    return metrics


def quartile(value: float, values: list[float]) -> int:
    if not values:
        return 1
    rank = percentile_ranks(values)[values.index(value)]
    if rank <= 25:
        return 1
    if rank <= 50:
        return 2
    if rank <= 75:
        return 3
    return 4
