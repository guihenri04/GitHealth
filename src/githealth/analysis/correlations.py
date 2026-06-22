from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from githealth.models import PullRequestMetrics


@dataclass(frozen=True)
class CorrelationResult:
    feature: str
    outcome: str
    coefficient: float | None
    description: str


def _strength(value: float | None) -> str:
    if value is None:
        return "amostra insuficiente"
    absolute = abs(value)
    if absolute < 0.2:
        return "muito fraca"
    if absolute < 0.4:
        return "fraca"
    if absolute < 0.6:
        return "moderada"
    if absolute < 0.8:
        return "forte"
    return "muito forte"


def _direction(value: float | None) -> str:
    if value is None:
        return "sem direcao"
    if value > 0:
        return "positiva"
    if value < 0:
        return "negativa"
    return "neutra"


def describe_association(feature: str, outcome: str, coefficient: float | None) -> str:
    if coefficient is None:
        return f"Nao houve amostra suficiente para associar {feature} e {outcome}."
    return (
        f"Foi encontrada associacao {_direction(coefficient)} {_strength(coefficient)} "
        f"entre {feature} e {outcome}."
    )


def calculate_correlations(metrics: list[PullRequestMetrics]) -> list[CorrelationResult]:
    rows = [
        {
            "churn": metric.churn,
            "changed_files": metric.changed_files,
            "commits": metric.commits,
            "change_size_index": metric.change_size_index,
            "review_effort_index": metric.review_effort_index,
            "first_review_hours": metric.first_review_hours,
            "cycle_hours": metric.cycle_hours,
        }
        for metric in metrics
    ]
    frame = pd.DataFrame(rows)
    pairs = [
        ("churn", "first_review_hours"),
        ("changed_files", "cycle_hours"),
        ("commits", "review_effort_index"),
        ("change_size_index", "cycle_hours"),
        ("review_effort_index", "cycle_hours"),
    ]
    results: list[CorrelationResult] = []
    for feature, outcome in pairs:
        coefficient: float | None
        if frame.empty or frame[[feature, outcome]].dropna().shape[0] < 3:
            coefficient = None
        else:
            value = frame[feature].corr(frame[outcome], method="spearman")
            coefficient = None if pd.isna(value) else round(float(value), 4)
        results.append(
            CorrelationResult(
                feature=feature,
                outcome=outcome,
                coefficient=coefficient,
                description=describe_association(feature, outcome, coefficient),
            )
        )
    return results
