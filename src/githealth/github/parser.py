from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from githealth.exceptions import InvalidRepositoryError

if TYPE_CHECKING:
    from githealth.models.file_change import FileChange
    from githealth.models.pull_request import PullRequest
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


def ready_at_from_events(detail: dict[str, Any], events: list[dict[str, Any]]) -> datetime:
    created_at = parse_datetime(detail["created_at"])
    ready_events = [
        parsed
        for event in events
        if event.get("event") == "ready_for_review"
        for parsed in [parse_datetime(event.get("created_at"))]
        if parsed is not None
    ]
    if ready_events:
        return min(ready_events)
    if created_at is None:
        raise ValueError("Pull request payload does not contain a valid created_at value.")
    return created_at


def parse_pull_request(
    detail: dict[str, Any],
    files: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    review_comments: list[dict[str, Any]],
    events: list[dict[str, Any]],
    commits: list[dict[str, Any]],
) -> PullRequest:
    from githealth.models.pull_request import PullRequest

    user = detail.get("user") or {}
    parsed_reviews = tuple(
        review for payload in reviews for review in [parse_review(payload)] if review is not None
    )
    commit_dates = []
    for payload in commits:
        commit = payload.get("commit") or {}
        committer = commit.get("committer", {})
        parsed = parse_datetime(committer.get("date"))
        if parsed is not None:
            commit_dates.append(parsed)

    created_at = parse_datetime(detail["created_at"])
    if created_at is None:
        raise ValueError("Pull request payload does not contain created_at.")

    return PullRequest(
        number=int(detail["number"]),
        title=detail.get("title", ""),
        author=user.get("login", "unknown"),
        author_type=user.get("type", "User"),
        created_at=created_at,
        ready_at=ready_at_from_events(detail, events),
        closed_at=parse_datetime(detail.get("closed_at")),
        merged_at=parse_datetime(detail.get("merged_at")),
        state="merged" if detail.get("merged_at") else detail.get("state", "closed"),
        commits=int(detail.get("commits", len(commits))),
        additions=int(detail.get("additions", 0)),
        deletions=int(detail.get("deletions", 0)),
        changed_files=int(detail.get("changed_files", len(files))),
        review_comments=len(review_comments),
        labels=tuple(
            label.get("name", "") for label in detail.get("labels", []) if label.get("name")
        ),
        reviews=parsed_reviews,
        files=tuple(parse_file_change(file_payload) for file_payload in files),
        commit_dates=tuple(commit_dates),
    )
