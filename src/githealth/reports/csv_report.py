from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path

from githealth.models import PullRequestMetrics


def write_pull_requests_csv(path: Path, metrics: list[PullRequestMetrics]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(asdict(metrics[0]).keys()) if metrics else [])
        if not metrics:
            file.write("")
            return
        writer.writeheader()
        for metric in metrics:
            row = asdict(metric)
            row["labels"] = ";".join(metric.labels)
            writer.writerow(row)
