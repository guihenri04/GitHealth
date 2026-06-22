from __future__ import annotations

from collections import defaultdict
from statistics import median

from githealth.models import FileHotspot, PullRequest, PullRequestMetrics


def _median_optional(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return round(float(median(present)), 4)


def calculate_file_hotspots(
    pull_requests: list[PullRequest],
    metrics: list[PullRequestMetrics],
    min_samples: int = 3,
) -> list[FileHotspot]:
    metrics_by_number = {metric.number: metric for metric in metrics}
    grouped: dict[str, list[PullRequestMetrics]] = defaultdict(list)

    for pr in pull_requests:
        metric = metrics_by_number.get(pr.number)
        if metric is None:
            continue
        for file_change in pr.files:
            grouped[file_change.filename].append(metric)

    hotspots = [
        FileHotspot(
            filename=filename,
            pull_requests=len(file_metrics),
            median_first_review_hours=_median_optional(
                [metric.first_review_hours for metric in file_metrics]
            ),
            median_cycle_hours=_median_optional([metric.cycle_hours for metric in file_metrics]),
            median_review_effort=round(
                float(median(metric.review_effort_index for metric in file_metrics)), 4
            ),
            changes_requested=sum(metric.changes_requested for metric in file_metrics),
            sample_sufficient=len(file_metrics) >= min_samples,
        )
        for filename, file_metrics in grouped.items()
    ]
    return sorted(
        hotspots,
        key=lambda item: (
            not item.sample_sufficient,
            -(item.median_cycle_hours or 0),
            -item.median_review_effort,
            item.filename,
        ),
    )
