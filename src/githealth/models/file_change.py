from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FileChange:
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int


@dataclass(frozen=True)
class FileHotspot:
    filename: str
    pull_requests: int
    median_first_review_hours: float | None
    median_cycle_hours: float | None
    median_review_effort: float
    changes_requested: int
    sample_sufficient: bool

