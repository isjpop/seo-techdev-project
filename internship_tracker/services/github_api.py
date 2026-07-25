"""GitHub API integration."""

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


def fetch_github_profile(access_token: str) -> dict[str, Any]:
    """
    Fetch GitHub user profile and repositories.

    Returns:
        Dict with name, username, email, profile_picture, repositories, repo_count.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    try:
        user_resp = requests.get(f"{GITHUB_API_BASE}/user", headers=headers, timeout=10)
        user_resp.raise_for_status()
        user_data = user_resp.json()

        repos_resp = requests.get(
            f"{GITHUB_API_BASE}/user/repos",
            headers=headers,
            params={"per_page": 100, "sort": "updated"},
            timeout=10,
        )
        repos_resp.raise_for_status()
        repos = repos_resp.json()

        profile = {
            "name": user_data.get("name") or user_data.get("login", ""),
            "username": user_data.get("login", ""),
            "email": user_data.get("email", ""),
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

    except requests.RequestException as exc:
        logger.error("GitHub API failure: %s", exc)
        raise


def fetch_github_email(access_token: str) -> str:
    """Fetch primary verified email from GitHub."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    try:
        resp = requests.get(f"{GITHUB_API_BASE}/user/emails", headers=headers, timeout=10)
        resp.raise_for_status()
        emails = resp.json()
        for entry in emails:
            if entry.get("primary") and entry.get("verified"):
                return entry["email"]
        if emails:
            return emails[0].get("email", "")
    except requests.RequestException as exc:
        logger.error("GitHub email fetch failure: %s", exc)

    return ""
