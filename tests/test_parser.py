from __future__ import annotations

from datetime import UTC, datetime

import pytest

from githealth.exceptions import InvalidRepositoryError
from githealth.github.parser import parse_repository, ready_at_from_events


def test_accepts_owner_repo() -> None:
    assert parse_repository("owner/repo") == ("owner", "repo")


def test_accepts_github_url() -> None:
    assert parse_repository("https://github.com/owner/repo") == ("owner", "repo")


def test_rejects_invalid_repository() -> None:
    with pytest.raises(InvalidRepositoryError):
        parse_repository("https://example.com/owner/repo")


def test_uses_ready_for_review_event_for_draft_pr() -> None:
    detail = {"created_at": "2026-01-01T10:00:00Z"}
    events = [
        {"event": "converted_to_draft", "created_at": "2026-01-01T11:00:00Z"},
        {"event": "ready_for_review", "created_at": "2026-01-01T12:00:00Z"},
    ]

    assert ready_at_from_events(detail, events) == datetime(2026, 1, 1, 12, tzinfo=UTC)
