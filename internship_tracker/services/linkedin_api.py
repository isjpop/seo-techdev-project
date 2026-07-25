"""LinkedIn API integration."""

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

LINKEDIN_API_BASE = "https://api.linkedin.com/v2"


def fetch_linkedin_profile(access_token: str) -> dict[str, Any]:
    """
    Fetch LinkedIn user profile data.

    Returns:
        Dict with full_name, headline, profile_picture, education, experience.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        profile_resp = requests.get(
            f"{LINKEDIN_API_BASE}/userinfo",
            headers=headers,
            timeout=10,
        )
        profile_resp.raise_for_status()
        data = profile_resp.json()

        profile = {
            "full_name": data.get("name", ""),
            "headline": data.get("headline", ""),
            "profile_picture": data.get("picture", ""),
            "email": data.get("email", ""),
            "sub": data.get("sub", ""),
            "education": [],
            "experience": [],
        }

        logger.info("Fetched LinkedIn profile for %s", profile["full_name"])
        return profile

    except requests.RequestException as exc:
        logger.error("LinkedIn API failure: %s", exc)
        raise
