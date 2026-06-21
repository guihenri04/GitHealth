from __future__ import annotations

from githealth.analysis.correlations import calculate_correlations, describe_association
from githealth.analysis.durations import build_all_metrics
from githealth.analysis.scores import apply_scores


def test_calculates_spearman_correlations(sample_prs) -> None:
    metrics = apply_scores(build_all_metrics(sample_prs))
    correlations = calculate_correlations(metrics)
    changed_files = next(item for item in correlations if item.feature == "changed_files")
    assert changed_files.coefficient is not None


def test_association_text_does_not_claim_causality() -> None:
    text = describe_association("arquivos modificados", "tempo ate merge", 0.5)
    assert "associacao" in text
    assert "causa" not in text
