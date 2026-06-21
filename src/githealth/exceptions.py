class GitHealthError(Exception):
    """Base exception for expected GitHealth failures."""


class InvalidRepositoryError(GitHealthError):
    """Raised when a repository identifier cannot be parsed."""


class GitHubAPIError(GitHealthError):
    """Raised when the GitHub API returns an error response."""


class GitHubRateLimitError(GitHubAPIError):
    """Raised when GitHub rate limits the current client."""


class MissingTokenError(GitHealthError):
    """Raised when an operation requires a token that was not configured."""

