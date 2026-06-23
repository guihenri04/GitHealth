from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from statistics import median

import plotly.express as px
from jinja2 import Environment, PackageLoader, select_autoescape

from githealth.analysis.correlations import CorrelationResult
from githealth.models import FileHotspot, PullRequestMetrics


def _median(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return round(float(median(present)), 2) if present else None


def _format_hours(value: float | None) -> str:
    if value is None:
        return "sem dados"
    total_minutes = round(value * 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours >= 24:
        days, remaining_hours = divmod(hours, 24)
        if remaining_hours == 0:
            return f"{days}d"
        return f"{days}d {remaining_hours}h"
    return f"{hours}h {minutes:02d}min"


def _summary(
    metrics: list[PullRequestMetrics],
    hotspots: list[FileHotspot],
) -> dict[str, str | int]:
    merged = [metric for metric in metrics if metric.state == "merged"]
    changes_requested = [metric for metric in metrics if metric.changes_requested > 0]
    change_rate = (len(changes_requested) / len(metrics) * 100) if metrics else 0
    return {
        "pull_requests": len(metrics),
        "merged": len(merged),
        "hotspots": len([hotspot for hotspot in hotspots if hotspot.sample_sufficient]),
        "change_request_rate": f"{change_rate:.1f}%",
        "median_first_review": _format_hours(_median([m.first_review_hours for m in metrics])),
        "median_cycle": _format_hours(_median([m.cycle_hours for m in metrics])),
    }


def _scatter(metrics: list[PullRequestMetrics]) -> str:
    rows = [
        {
            "PR": metric.number,
            "Arquivos": metric.changed_files,
            "Indice de tamanho": metric.change_size_index,
            "Horas ate encerramento": metric.cycle_hours,
            "Indice de esforco": metric.review_effort_index,
        }
        for metric in metrics
        if metric.cycle_hours is not None
    ]
    if not rows:
        return ""
    figure = px.scatter(
        rows,
        x="Indice de tamanho",
        y="Horas ate encerramento",
        size="Arquivos",
        hover_name="PR",
        title="Indice de tamanho x tempo do PR",
        color="Indice de esforco",
        color_continuous_scale="Tealrose",
    )
    figure.update_layout(
        margin={"l": 32, "r": 18, "t": 52, "b": 32},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Inter, Arial, sans-serif", "size": 13},
    )
    return figure.to_html(full_html=False, include_plotlyjs="cdn")


def _bar(hotspots: list[FileHotspot]) -> str:
    rows = [
        {
            "Arquivo": hotspot.filename,
            "Horas": hotspot.median_cycle_hours,
            "PRs": hotspot.pull_requests,
        }
        for hotspot in hotspots
        if hotspot.sample_sufficient and hotspot.median_cycle_hours is not None
    ][:10]
    if not rows:
        return ""
    figure = px.bar(
        rows,
        x="Horas",
        y="Arquivo",
        orientation="h",
        title="Arquivos com maior tempo mediano de ciclo",
        color="PRs",
        color_continuous_scale="Bluyl",
    )
    figure.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin={"l": 32, "r": 18, "t": 52, "b": 32},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Inter, Arial, sans-serif", "size": 13},
    )
    return figure.to_html(full_html=False, include_plotlyjs=False)


def write_html_report(
    path: Path,
    repository: str,
    metrics: list[PullRequestMetrics],
    hotspots: list[FileHotspot],
    correlations: list[CorrelationResult],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    environment = Environment(
        loader=PackageLoader("githealth", "reports/templates"),
        autoescape=select_autoescape(),
    )
    environment.filters["duration"] = _format_hours
    template = environment.get_template("report.html.j2")
    rendered = template.render(
        repository=repository,
        summary=_summary(metrics, hotspots),
        metrics=[asdict(metric) for metric in metrics],
        hotspots=[asdict(hotspot) for hotspot in hotspots],
        correlations=[asdict(result) for result in correlations],
        scatter_chart=_scatter(metrics),
        hotspot_chart=_bar(hotspots),
    )
    path.write_text(rendered, encoding="utf-8")
