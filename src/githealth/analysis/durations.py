from __future__ import annotations

from datetime import datetime

from githealth.models import PullRequest, PullRequestMetrics, Review


def hours_between(start: datetime | None, end: datetime | None) -> float | None:
    if start is None or end is None or end < start:
        return None
    return round((end - start).total_seconds() / 3600, 4)


def first_review(reviews: tuple[Review, ...], ready_at: datetime) -> Review | None:
    submitted = [review for review in reviews if review.submitted_at >= ready_at]
    return min(submitted, key=lambda review: review.submitted_at, default=None)


def build_pull_request_metrics(pr: PullRequest) -> PullRequestMetrics:
    first = first_review(pr.reviews, pr.ready_at)
    first_review_at = first.submitted_at if first else None
    terminal_at = pr.merged_at or pr.closed_at

    return PullRequestMetrics(
        number=pr.number,
        title=pr.title,
        author=pr.author,
        state=pr.state,
        created_at=pr.created_at,
        ready_at=pr.ready_at,
        first_review_at=first_review_at,
        closed_at=pr.closed_at,
        merged_at=pr.merged_at,
        first_review_hours=hours_between(pr.ready_at, first_review_at),
        cycle_hours=hours_between(pr.ready_at, terminal_at),
        post_review_hours=hours_between(first_review_at, terminal_at),
        commits=pr.commits,
        changed_files=pr.changed_files,
        additions=pr.additions,
        deletions=pr.deletions,
        churn=pr.churn,
        number_of_reviews=len(pr.reviews),
        changes_requested=sum(1 for review in pr.reviews if review.state == "CHANGES_REQUESTED"),
        review_comments=pr.review_comments,
        commits_after_first_review=0,
        labels=pr.labels,
    )


def build_all_metrics(pull_requests: list[PullRequest]) -> list[PullRequestMetrics]:
    return [build_pull_request_metrics(pr) for pr in pull_requests]
