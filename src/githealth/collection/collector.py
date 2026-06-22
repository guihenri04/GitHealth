from __future__ import annotations

from typing import TYPE_CHECKING

from githealth.config import AnalysisConfig
from githealth.github.client import GitHubClient
from githealth.github.parser import parse_pull_request

if TYPE_CHECKING:
    from githealth.models.pull_request import PullRequest


class PullRequestCollector:
    def __init__(self, client: GitHubClient) -> None:
        self.client = client

    def collect(self, config: AnalysisConfig) -> list[PullRequest]:
        path = f"/repos/{config.owner}/{config.repo}/pulls"
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
            "per_page": 100,
        }
        numbers = [
            int(item["number"])
            for item in self.client.paginate(path, params=params, limit=config.limit)
            if self._inside_interval(item, config)
        ]

        pull_requests: list[PullRequest] = []
        for number in numbers:
            pull_requests.append(self.collect_one(config.owner, config.repo, number))
        return pull_requests

    def collect_one(self, owner: str, repo: str, number: int) -> PullRequest:
        detail = self.client.get_json(f"/repos/{owner}/{repo}/pulls/{number}")
        files = list(self.client.paginate(f"/repos/{owner}/{repo}/pulls/{number}/files"))
        reviews = list(self.client.paginate(f"/repos/{owner}/{repo}/pulls/{number}/reviews"))
        review_comments = list(
            self.client.paginate(f"/repos/{owner}/{repo}/pulls/{number}/comments")
        )
        events = list(self.client.paginate(f"/repos/{owner}/{repo}/issues/{number}/events"))
        commits = list(self.client.paginate(f"/repos/{owner}/{repo}/pulls/{number}/commits"))
        return parse_pull_request(detail, files, reviews, review_comments, events, commits)

    @staticmethod
    def _inside_interval(item: dict[str, object], config: AnalysisConfig) -> bool:
        from githealth.github.parser import parse_datetime

        closed_value = item.get("closed_at")
        closed_at = parse_datetime(closed_value if isinstance(closed_value, str) else None)
        if closed_at is None:
            return False
        if config.since and closed_at < config.since:
            return False
        return not (config.until and closed_at >= config.until)
