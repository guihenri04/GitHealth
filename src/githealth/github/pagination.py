from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def get_next_url(link_header: str | None) -> str | None:
    if not link_header:
        return None

    for part in link_header.split(","):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        url_part = section.split(";", maxsplit=1)[0].strip()
        return url_part.removeprefix("<").removesuffix(">")
    return None


def merge_query_params(url: str, params: dict[str, str | int | None]) -> dict[str, str | int]:
    existing = parse_qs(urlparse(url).query)
    merged: dict[str, str | int] = {}
    for key, value in existing.items():
        if value:
            merged[key] = value[-1]
    for key, value in params.items():
        if value is not None:
            merged[key] = value
    return merged
