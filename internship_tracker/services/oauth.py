"""OAuth 2.0 configuration and helpers."""

import logging
from urllib.parse import unquote_plus

from authlib.integrations.flask_client import OAuth
from flask import current_app, flash, redirect, request, url_for

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
        server_metadata_url=app.config["LINKEDIN_SERVER_METADATA_URL"],
        access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
        authorize_url="https://www.linkedin.com/oauth/v2/authorization",
        api_base_url="https://api.linkedin.com/",
        client_kwargs={
            "scope": "openid profile email",
            "token_endpoint_auth_method": "client_secret_post",
        },
    )


def get_redirect_uri(provider: str) -> str:
    """Build OAuth callback redirect URI."""
    base = current_app.config["OAUTH_REDIRECT_BASE"].rstrip("/")
    return f"{base}/auth/callback/{provider}"


def handle_oauth_error(provider: str, error: Exception):
    """Handle OAuth failures with user-friendly messages."""
    provider_name = provider.title()
    query_error = request.args.get("error")
    query_description = request.args.get("error_description")
    details = query_description or query_error or str(error)

    if query_description:
        details = unquote_plus(query_description)

    logger.error(
        "OAuth error for %s. query_error=%s query_description=%s exception=%s",
        provider,
        query_error,
        details,
        error,
    )

    if details:
        flash(f"{provider_name} authentication failed: {details}", "error")
    else:
        flash(f"Authentication with {provider_name} failed. Please try again.", "error")
    return redirect(url_for("auth.login"))
