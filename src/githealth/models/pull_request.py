from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from githealth.models.file_change import FileChange
from githealth.models.review import Review


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    author: str
    author_type: str
    created_at: datetime
    ready_at: datetime
    closed_at: datetime | None
    merged_at: datetime | None
    state: str
    commits: int
    additions: int
    deletions: int
    changed_files: int
    review_comments: int
    labels: tuple[str, ...] = ()
    reviews: tuple[Review, ...] = ()
    files: tuple[FileChange, ...] = ()
    commit_dates: tuple[datetime, ...] = ()

    @property
    def is_merged(self) -> bool:
        return self.merged_at is not None

    @property
    def is_bot(self) -> bool:
        return self.author_type.lower() == "bot" or self.author.endswith("[bot]")

    @property
    def churn(self) -> int:
        return self.additions + self.deletions
