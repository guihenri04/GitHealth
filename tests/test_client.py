from __future__ import annotations

import httpx
import pytest

from githealth.config import GitHubConfig
from githealth.exceptions import GitHubAPIError, GitHubRateLimitError
from githealth.github.client import GitHubClient
from githealth.github.pagination import get_next_url


def test_client_creates_authorization_header() -> None:
    client = GitHubClient(GitHubConfig(token="abc"))
    try:
        assert client.headers["Authorization"] == "Bearer abc"
    finally:
        client.close()


def test_get_next_url_from_link_header() -> None:
    link = '<https://api.github.com/items?page=2>; rel="next", <x?page=5>; rel="last"'
    assert get_next_url(link) == "https://api.github.com/items?page=2"


def test_pagination_reads_multiple_pages() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json=[{"id": 2}])
        return httpx.Response(
            200,
            json=[{"id": 1}],
            headers={"link": '<https://api.github.com/items?page=2>; rel="next"'},
        )

    client = GitHubClient(GitHubConfig(token=None), transport=httpx.MockTransport(handler))
    try:
        assert list(client.paginate("/items")) == [{"id": 1}, {"id": 2}]
    finally:
        client.close()


def test_401_raises_api_error() -> None:
    client = GitHubClient(
        GitHubConfig(token=None),
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(401, json={"message": "bad"})
        ),
    )
    try:
        with pytest.raises(GitHubAPIError):
            client.get_json("/bad")
    finally:
        client.close()


def test_rate_limit_raises_specific_error() -> None:
    client = GitHubClient(
        GitHubConfig(token=None),
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(403, headers={"x-ratelimit-remaining": "0"})
        ),
    )
    try:
        with pytest.raises(GitHubRateLimitError):
            client.get_json("/limited")
    finally:
        client.close()
