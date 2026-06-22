from __future__ import annotations

import httpx

from githealth.config import GitHubConfig


class GitHubClient:
    def __init__(self, config: GitHubConfig, transport: httpx.BaseTransport | None = None) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "githealth-cli",
        }
        if config.token:
            headers["Authorization"] = f"Bearer {config.token}"

        self._client = httpx.Client(
            base_url=config.api_url,
            headers=headers,
            timeout=config.timeout,
            transport=transport,
        )

    @property
    def headers(self) -> httpx.Headers:
        return self._client.headers

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()
