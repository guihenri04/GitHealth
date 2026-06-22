from __future__ import annotations

from statistics import median

from rich.console import Console
from rich.table import Table

from githealth.analysis.correlations import CorrelationResult
from githealth.models import FileHotspot, PullRequestMetrics


def _format_hours(value: float | None) -> str:
    if value is None:
        return "sem dados"
    total_minutes = round(value * 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes:02d}min"


def _median(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return float(median(present)) if present else None


def render_summary(
    repository: str,
    metrics: list[PullRequestMetrics],
    hotspots: list[FileHotspot],
    correlations: list[CorrelationResult],
    console: Console | None = None,
) -> None:
    console = console or Console()
    merged = [metric for metric in metrics if metric.state == "merged"]
    changed = [metric for metric in metrics if metric.changes_requested > 0]
    console.print(f"[bold]GitHealth — {repository}[/bold]\n")
    console.print(f"Pull requests analisados: {len(metrics)}")
    console.print(f"PRs merged: {len(merged)}")
    first_review = _format_hours(_median([m.first_review_hours for m in metrics]))
    cycle = _format_hours(_median([m.cycle_hours for m in metrics]))
    console.print(f"Mediana ate primeira revisao: {first_review}")
    console.print(f"Mediana ate encerramento/merge: {cycle}")
    percentage = round((len(changed) / len(metrics)) * 100, 1) if metrics else 0
    console.print(f"PRs com pedido de alteracao: {percentage}%\n")

    corr_table = Table(title="Associacoes mais relevantes")
    corr_table.add_column("Caracteristica")
    corr_table.add_column("Resultado")
    corr_table.add_column("Spearman", justify="right")
    for result in sorted(
        correlations,
        key=lambda item: abs(item.coefficient or 0),
        reverse=True,
    )[:5]:
        coefficient = "n/a" if result.coefficient is None else f"{result.coefficient:.2f}"
        corr_table.add_row(result.feature, result.outcome, coefficient)
    console.print(corr_table)

    hotspot_table = Table(title="Arquivos associados aos maiores atrasos")
    hotspot_table.add_column("Arquivo")
    hotspot_table.add_column("PRs", justify="right")
    hotspot_table.add_column("Mediana ciclo", justify="right")
    hotspot_table.add_column("Esforco", justify="right")
    for hotspot in [item for item in hotspots if item.sample_sufficient][:10]:
        hotspot_table.add_row(
            hotspot.filename,
            str(hotspot.pull_requests),
            _format_hours(hotspot.median_cycle_hours),
            f"{hotspot.median_review_effort:.1f}",
        )
    console.print(hotspot_table)
