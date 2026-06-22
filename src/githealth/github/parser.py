from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from githealth.exceptions import InvalidRepositoryError

if TYPE_CHECKING:
    from githealth.models.file_change import FileChange
    from githealth.models.review import Review

REPO_PATTERN = re.compile(
    r"^(?:https://github\.com/)?(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)


def parse_repository(value: str) -> tuple[str, str]:
    match = REPO_PATTERN.match(value.strip())
    if not match:
        raise InvalidRepositoryError(
            "Use o formato 'owner/repository' ou 'https://github.com/owner/repository'."
        )
    return match.group("owner"), match.group("repo")


def parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def parse_file_change(payload: dict[str, Any]) -> FileChange:
    from githealth.models.file_change import FileChange

    return FileChange(
        filename=payload["filename"],
        status=payload.get("status", "modified"),
        additions=int(payload.get("additions", 0)),
        deletions=int(payload.get("deletions", 0)),
        changes=int(payload.get("changes", 0)),
    )


def parse_review(payload: dict[str, Any]) -> Review | None:
    from githealth.models.review import Review

    submitted_at = parse_datetime(payload.get("submitted_at"))
    user = payload.get("user") or {}
    if submitted_at is None:
        return None
    return Review(
        reviewer=user.get("login", "unknown"),
        state=payload.get("state", "UNKNOWN"),
        submitted_at=submitted_at,
    )
