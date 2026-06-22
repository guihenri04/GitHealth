from __future__ import annotations

import json

from githealth.analysis import (
    apply_scores,
    build_all_metrics,
    calculate_correlations,
    calculate_file_hotspots,
)
from githealth.reports import (
    write_analysis_json,
    write_file_hotspots_csv,
    write_html_report,
    write_pull_requests_csv,
)


def test_exports_csv_json_and_html(tmp_path, sample_prs) -> None:
    metrics = apply_scores(build_all_metrics(sample_prs))
    hotspots = calculate_file_hotspots(sample_prs, metrics, min_samples=2)
    correlations = calculate_correlations(metrics)

    write_pull_requests_csv(tmp_path / "pull_requests.csv", metrics)
    write_file_hotspots_csv(tmp_path / "file_hotspots.csv", hotspots)
    write_analysis_json(tmp_path / "analysis.json", "owner/repo", metrics, hotspots, correlations)
    write_html_report(tmp_path / "summary.html", "owner/repo", metrics, hotspots, correlations)

    assert "Large refactor" in (tmp_path / "pull_requests.csv").read_text(encoding="utf-8")
    analysis = json.loads((tmp_path / "analysis.json").read_text(encoding="utf-8"))
    assert analysis["repository"] == "owner/repo"
    assert "GitHealth" in (tmp_path / "summary.html").read_text(encoding="utf-8")
