from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from pathlib import Path


@dataclass(frozen=True)
class GitHubConfig:
    token: str | None
    api_url: str = "https://api.github.com"
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> GitHubConfig:
        return cls(token=os.getenv("GITHUB_TOKEN"))


@dataclass(frozen=True)
class AnalysisConfig:
    owner: str
    repo: str
    output: Path
    since: datetime | None = None
    until: datetime | None = None
    include_bots: bool = False
    min_file_samples: int = 3
    limit: int | None = None


def parse_date(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = date.fromisoformat(value)
    return datetime.combine(parsed, time.min, tzinfo=UTC)

