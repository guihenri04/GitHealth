from __future__ import annotations

import pytest

from githealth.exceptions import InvalidRepositoryError
from githealth.github.parser import parse_repository


def test_accepts_owner_repo() -> None:
    assert parse_repository("owner/repo") == ("owner", "repo")


def test_accepts_github_url() -> None:
    assert parse_repository("https://github.com/owner/repo") == ("owner", "repo")


def test_rejects_invalid_repository() -> None:
    with pytest.raises(InvalidRepositoryError):
        parse_repository("https://example.com/owner/repo")
