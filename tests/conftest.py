from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from typer.testing import CliRunner

from githealth.models import FileChange, PullRequest, Review


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def dt(hour: int) -> datetime:
    return datetime(2026, 1, 1, hour, tzinfo=UTC)


@pytest.fixture
def sample_prs() -> list[PullRequest]:
    base = dt(8)
    return [
        PullRequest(
            number=1,
            title="Small fix",
            author="alice",
            author_type="User",
            created_at=base,
            ready_at=base,
            closed_at=base + timedelta(hours=4),
            merged_at=base + timedelta(hours=4),
            state="merged",
            commits=1,
            additions=10,
            deletions=2,
            changed_files=1,
            review_comments=1,
            reviews=(Review("bob", "APPROVED", base + timedelta(hours=1)),),
            files=(FileChange("src/a.py", "modified", 10, 2, 12),),
            commit_dates=(base,),
        ),
        PullRequest(
            number=2,
            title="Large refactor",
            author="carol",
            author_type="User",
            created_at=base,
            ready_at=base + timedelta(hours=2),
            closed_at=base + timedelta(hours=30),
            merged_at=base + timedelta(hours=30),
            state="merged",
            commits=5,
            additions=400,
            deletions=120,
            changed_files=8,
            review_comments=9,
            reviews=(
                Review("dan", "CHANGES_REQUESTED", base + timedelta(hours=5)),
                Review("dan", "APPROVED", base + timedelta(hours=20)),
            ),
            files=(
                FileChange("src/a.py", "modified", 100, 40, 140),
                FileChange("src/b.py", "modified", 300, 80, 380),
            ),
            commit_dates=(base + timedelta(hours=10), base + timedelta(hours=12)),
        ),
        PullRequest(
            number=3,
            title="Schema update",
            author="eve",
            author_type="User",
            created_at=base,
            ready_at=base,
            closed_at=base + timedelta(hours=50),
            merged_at=None,
            state="closed",
            commits=3,
            additions=200,
            deletions=100,
            changed_files=4,
            review_comments=4,
            reviews=(Review("frank", "COMMENTED", base + timedelta(hours=10)),),
            files=(
                FileChange("src/a.py", "modified", 100, 20, 120),
                FileChange("db/schema.sql", "modified", 100, 80, 180),
            ),
            commit_dates=(base + timedelta(hours=2), base + timedelta(hours=15)),
        ),
    ]

