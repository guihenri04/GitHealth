from __future__ import annotations

import re

from githealth.exceptions import InvalidRepositoryError

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
