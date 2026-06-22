from __future__ import annotations

from githealth.analysis.durations import build_all_metrics
from githealth.analysis.hotspots import calculate_file_hotspots
from githealth.analysis.scores import apply_scores


def test_ignores_file_with_insufficient_sample(sample_prs) -> None:
    metrics = apply_scores(build_all_metrics(sample_prs))
    hotspots = calculate_file_hotspots(sample_prs, metrics, min_samples=3)
    schema = next(item for item in hotspots if item.filename == "db/schema.sql")
    assert not schema.sample_sufficient


def test_sorts_hotspots_with_sufficient_samples_first(sample_prs) -> None:
    metrics = apply_scores(build_all_metrics(sample_prs))
    hotspots = calculate_file_hotspots(sample_prs, metrics, min_samples=2)
    assert hotspots[0].filename == "src/a.py"
    assert hotspots[0].sample_sufficient
