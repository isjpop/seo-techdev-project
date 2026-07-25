"""OAuth 2.0 configuration and helpers."""

import logging

from authlib.integrations.flask_client import OAuth
from flask import current_app, flash, redirect, url_for

logger = logging.getLogger(__name__)

oauth = OAuth()


def init_oauth(app):
    """Register OAuth providers with the Flask app."""
    oauth.init_app(app)

    oauth.register(
        name="github",
        client_id=app.config["GITHUB_CLIENT_ID"],
        client_secret=app.config["GITHUB_CLIENT_SECRET"],
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email read:user repo"},
    )

    oauth.register(
        name="linkedin",
        client_id=app.config["LINKEDIN_CLIENT_ID"],
        client_secret=app.config["LINKEDIN_CLIENT_SECRET"],
        access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
        authorize_url="https://www.linkedin.com/oauth/v2/authorization",
        api_base_url="https://api.linkedin.com/",
        client_kwargs={"scope": "openid profile email"},
    )


def get_redirect_uri(provider: str) -> str:
    """Build OAuth callback redirect URI."""
    base = current_app.config["OAUTH_REDIRECT_BASE"].rstrip("/")
    return f"{base}/auth/callback/{provider}"


def handle_oauth_error(provider: str, error: Exception):
    """Handle OAuth failures with user-friendly messages."""
    logger.error("OAuth error for %s: %s", provider, error)
    flash(f"Authentication with {provider.title()} failed. Please try again.", "error")
    return redirect(url_for("auth.login"))
