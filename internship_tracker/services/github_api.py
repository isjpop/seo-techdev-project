"""GitHub API integration."""

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"
MAX_REPO_PAGES = 10  # safety cap: 10 pages * 100/page = up to 1000 repos fetched


class GitHubAPIError(Exception):
    """Base exception for GitHub API failures."""


class GitHubAuthError(GitHubAPIError):
    """Raised when the GitHub access token is invalid or expired."""


class GitHubRateLimitError(GitHubAPIError):
    """Raised when the GitHub API rate limit has been exceeded."""


def _github_session(access_token: str) -> requests.Session:
    """Build a requests Session pre-configured with GitHub auth headers."""
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }
    )
    return session


def _raise_for_github_status(resp: requests.Response) -> None:
    """Translate common GitHub error responses into specific exceptions."""
    if resp.status_code == 401:
        logger.warning("GitHub token invalid or expired")
        raise GitHubAuthError("GitHub access token is invalid or expired")
    if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
        logger.warning("GitHub API rate limit exceeded")
        raise GitHubRateLimitError("GitHub API rate limit exceeded")
    resp.raise_for_status()


def _fetch_all_repos(session: requests.Session) -> list[dict[str, Any]]:
    """Fetch all of the user's repositories, following pagination."""
    all_repos: list[dict[str, Any]] = []
    page = 1

    while page <= MAX_REPO_PAGES:
        resp = session.get(
            f"{GITHUB_API_BASE}/user/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
            timeout=10,
        )
        _raise_for_github_status(resp)
        batch = resp.json()
        all_repos.extend(batch)

        if len(batch) < 100:
            break  # last page reached
        page += 1

    return all_repos


def fetch_github_profile(access_token: str) -> dict[str, Any]:
    """
    Fetch GitHub user profile and repositories.

    Returns:
        Dict with name, username, email, profile_picture, repositories, repo_count.

    Raises:
        GitHubAuthError: if the access token is invalid or expired.
        GitHubRateLimitError: if the GitHub API rate limit has been exceeded.
        GitHubAPIError: for other GitHub API/network failures.
    """
    session = _github_session(access_token)

    try:
        user_resp = session.get(f"{GITHUB_API_BASE}/user", timeout=10)
        _raise_for_github_status(user_resp)
        user_data = user_resp.json()

        repos = _fetch_all_repos(session)

        # GitHub only returns `email` on /user if the user made it public.
        # Fall back to the verified primary address from /user/emails.
        email = user_data.get("email") or fetch_github_email(access_token)

        profile = {
            "name": user_data.get("name") or user_data.get("login", ""),
            "username": user_data.get("login", ""),
            "email": email,
            "profile_picture": user_data.get("avatar_url", ""),
            "bio": user_data.get("bio", ""),
            "public_repos": user_data.get("public_repos", 0),
            "repo_count": len(repos),
            "repositories": [
                {
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "url": r.get("html_url"),
                    "stars": r.get("stargazers_count", 0),
                    "language": r.get("language"),
                }
                for r in repos[:20]
            ],
        }
        logger.info("Fetched GitHub profile for %s", profile["username"])
        return profile

    except GitHubAPIError:
        raise
    except requests.RequestException as exc:
        logger.error("GitHub API failure: %s", exc)
        raise GitHubAPIError(str(exc)) from exc
    finally:
        session.close()


def fetch_github_email(access_token: str) -> str:
    """
    Fetch primary verified email from GitHub.

    Raises:
        GitHubAuthError: if the access token is invalid or expired.
        GitHubRateLimitError: if the GitHub API rate limit has been exceeded.
        GitHubAPIError: for other GitHub API/network failures.
    """
    session = _github_session(access_token)

    try:
        resp = session.get(f"{GITHUB_API_BASE}/user/emails", timeout=10)
        _raise_for_github_status(resp)
        emails = resp.json()

        for entry in emails:
            if entry.get("primary") and entry.get("verified"):
                return entry["email"]
        if emails:
            return emails[0].get("email", "")
        return ""

    except GitHubAPIError:
        raise
    except requests.RequestException as exc:
        logger.error("GitHub email fetch failure: %s", exc)
        raise GitHubAPIError(str(exc)) from exc
    finally:
        session.close()