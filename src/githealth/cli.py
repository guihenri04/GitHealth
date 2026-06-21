from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from githealth.analysis import (
    apply_scores,
    build_all_metrics,
    calculate_correlations,
    calculate_file_hotspots,
)
from githealth.collection.collector import PullRequestCollector
from githealth.config import AnalysisConfig, GitHubConfig, parse_date
from githealth.exceptions import GitHealthError
from githealth.github.client import GitHubClient
from githealth.github.parser import parse_repository
from githealth.reports import (
    render_summary,
    write_analysis_json,
    write_file_hotspots_csv,
    write_html_report,
    write_pull_requests_csv,
)

app = typer.Typer(help="Mine GitHub pull requests to find review bottlenecks.")
console = Console()


def _run_analysis(config: AnalysisConfig) -> None:
    github_config = GitHubConfig.from_env()
    with GitHubClient(github_config) as client:
        collector = PullRequestCollector(client)
        pull_requests = collector.collect(config)

    metrics = apply_scores(build_all_metrics(pull_requests))
    correlations = calculate_correlations(metrics)
    hotspots = calculate_file_hotspots(pull_requests, metrics, config.min_file_samples)
    repository = f"{config.owner}/{config.repo}"

    config.output.mkdir(parents=True, exist_ok=True)
    write_pull_requests_csv(config.output / "pull_requests.csv", metrics)
    write_file_hotspots_csv(config.output / "file_hotspots.csv", hotspots)
    write_analysis_json(
        config.output / "analysis.json",
        repository,
        metrics,
        hotspots,
        correlations,
    )
    write_html_report(config.output / "summary.html", repository, metrics, hotspots, correlations)
    render_summary(repository, metrics, hotspots, correlations, console=console)
    console.print(f"\nRelatorios gerados em: [bold]{config.output}[/bold]")


@app.command()
def analyze(
    repository: str = typer.Argument(..., help="Repository as owner/repo or GitHub URL."),
    since: Annotated[
        str | None,
        typer.Option(help="Start date in YYYY-MM-DD format."),
    ] = None,
    until: Annotated[
        str | None,
        typer.Option(help="End date in YYYY-MM-DD format."),
    ] = None,
    output: Annotated[Path, typer.Option(help="Output directory.")] = Path("reports"),
    include_bots: Annotated[
        bool,
        typer.Option(help="Include pull requests opened by bots."),
    ] = False,
    min_file_samples: Annotated[
        int,
        typer.Option(help="Minimum PR sample for file hotspots."),
    ] = 3,
    limit: Annotated[
        int | None,
        typer.Option(help="Maximum number of PRs to collect."),
    ] = None,
) -> None:
    """Analyze closed pull requests from a GitHub repository."""
    try:
        owner, repo = parse_repository(repository)
        config = AnalysisConfig(
            owner=owner,
            repo=repo,
            output=output,
            since=parse_date(since),
            until=parse_date(until),
            include_bots=include_bots,
            min_file_samples=min_file_samples,
            limit=limit,
        )
        _run_analysis(config)
    except GitHealthError as error:
        console.print(f"[red]Erro:[/red] {error}")
        raise typer.Exit(code=1) from error
    except ValueError as error:
        console.print(f"[red]Erro de entrada:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command()
def inspect(
    repository: str = typer.Argument(..., help="Repository as owner/repo or GitHub URL."),
    number: int = typer.Argument(..., help="Pull request number."),
) -> None:
    """Inspect metrics for a single pull request."""
    try:
        owner, repo = parse_repository(repository)
        with GitHubClient(GitHubConfig.from_env()) as client:
            pr = PullRequestCollector(client).collect_one(owner, repo, number)
        metrics = apply_scores(build_all_metrics([pr]))[0]
        console.print(f"[bold]PR #{metrics.number} — {metrics.title}[/bold]")
        console.print(f"Autor: {metrics.author}")
        console.print(f"Estado: {metrics.state}")
        console.print(f"Arquivos alterados: {metrics.changed_files}")
        console.print(f"Churn: {metrics.churn}")
        console.print(f"Horas ate primeira revisao: {metrics.first_review_hours}")
        console.print(f"Horas ate encerramento/merge: {metrics.cycle_hours}")
        console.print(f"Indice de tamanho: {metrics.change_size_index}")
        console.print(f"Indice de esforco: {metrics.review_effort_index}")
    except GitHealthError as error:
        console.print(f"[red]Erro:[/red] {error}")
        raise typer.Exit(code=1) from error


@app.command()
def doctor() -> None:
    """Validate local configuration."""
    config = GitHubConfig.from_env()
    if config.token:
        console.print("[green]GITHUB_TOKEN configurado.[/green]")
    else:
        console.print(
            "[yellow]GITHUB_TOKEN nao configurado. O limite anonimo da API e menor.[/yellow]"
        )
    console.print("Python package: githealth")
    console.print(f"GitHub API: {config.api_url}")


if __name__ == "__main__":
    app()
