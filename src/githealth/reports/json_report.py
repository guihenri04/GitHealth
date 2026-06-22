from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from githealth.analysis.correlations import CorrelationResult
from githealth.models import FileHotspot, PullRequestMetrics


def _default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def write_analysis_json(
    path: Path,
    repository: str,
    metrics: list[PullRequestMetrics],
    hotspots: list[FileHotspot],
    correlations: list[CorrelationResult],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "repository": repository,
        "pull_requests": [asdict(metric) for metric in metrics],
        "file_hotspots": [asdict(hotspot) for hotspot in hotspots],
        "correlations": [asdict(result) for result in correlations],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default), encoding="utf-8")
