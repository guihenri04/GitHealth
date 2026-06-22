from __future__ import annotations


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
