from __future__ import annotations

from githealth.github.pagination import get_next_url


def test_get_next_url_from_link_header() -> None:
    link = '<https://api.github.com/items?page=2>; rel="next", <x?page=5>; rel="last"'
    assert get_next_url(link) == "https://api.github.com/items?page=2"
