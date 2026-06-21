from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FileChange:
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int

