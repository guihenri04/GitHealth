from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path

from githealth.models import FileHotspot, PullRequestMetrics


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


def write_file_hotspots_csv(path: Path, hotspots: list[FileHotspot]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(asdict(hotspots[0]).keys()) if hotspots else [])
        if not hotspots:
            file.write("")
            return
        writer.writeheader()
        for hotspot in hotspots:
            writer.writerow(asdict(hotspot))
