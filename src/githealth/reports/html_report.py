from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import plotly.express as px
from jinja2 import Environment, PackageLoader, select_autoescape

from githealth.analysis.correlations import CorrelationResult
from githealth.models import FileHotspot, PullRequestMetrics


def _scatter(metrics: list[PullRequestMetrics]) -> str:
    rows = [
        {
            "PR": metric.number,
            "Arquivos": metric.changed_files,
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
        x="Arquivos",
        y="Horas ate encerramento",
        size="Indice de esforco",
        hover_name="PR",
        title="Arquivos modificados x tempo do PR",
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
        rows, x="Horas", y="Arquivo", orientation="h", title="Hotspots por tempo mediano"
    )
    figure.update_layout(yaxis={"categoryorder": "total ascending"})
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
    template = environment.get_template("report.html.j2")
    rendered = template.render(
        repository=repository,
        metrics=[asdict(metric) for metric in metrics],
        hotspots=[asdict(hotspot) for hotspot in hotspots],
        correlations=[asdict(result) for result in correlations],
        scatter_chart=_scatter(metrics),
        hotspot_chart=_bar(hotspots),
    )
    path.write_text(rendered, encoding="utf-8")
