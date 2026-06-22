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
        summaries = [
            item
            for item in self.client.paginate(path, params=params, limit=config.limit)
            if self._inside_interval(item, config)
        ]
        return [parse_pull_request(item, [], [], [], [], []) for item in summaries]

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
