from __future__ import annotations

from githealth.config import GitHubConfig
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
