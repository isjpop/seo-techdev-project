"""Authentication tests."""

from services.oauth import handle_oauth_error
from flask import get_flashed_messages


def test_login_page_renders(client):
    """Login page should be accessible without authentication."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Internship Tracker" in response.data
    assert b"GitHub" in response.data
    assert b"LinkedIn" in response.data


def test_dashboard_requires_auth(client):
    """Dashboard should redirect unauthenticated users to login."""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_logout_redirects(client, auth_client):
    """Logout should redirect to login page."""
    client, _ = auth_client
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Internship Tracker" in response.data


def test_handle_oauth_error_uses_provider_error_message(app):
    """OAuth helper should surface provider error details when available."""
    with app.test_request_context(
        "/auth/callback/linkedin?error=access_denied&error_description=Bad+scope"
    ):
        response = handle_oauth_error("linkedin", Exception("oauth failed"))

        assert response.status_code == 302
        assert response.location.endswith("/login")

        messages = get_flashed_messages(with_categories=True)
        assert messages == [("error", "LinkedIn authentication failed: Bad scope")]


def test_linkedin_oidc_metadata_configured(app):
    """LinkedIn OAuth client should use the provider metadata document."""
    assert (
        app.config["LINKEDIN_SERVER_METADATA_URL"]
        == "https://www.linkedin.com/oauth/.well-known/openid-configuration"
    )


def test_handle_oauth_error_falls_back_to_exception_message(app):
    """When the provider gives no query error, the exception message should be used."""
    with app.test_request_context("/auth/callback/github"):
        response = handle_oauth_error("github", Exception("token exchange failed"))

        messages = get_flashed_messages(with_categories=True)
        assert messages == [("error", "GitHub authentication failed: token exchange failed")]


def test_handle_oauth_error_generic_message_when_no_details(app):
    """When there's no query error and the exception has no message, use the generic copy."""
    with app.test_request_context("/auth/callback/github"):
        response = handle_oauth_error("github", Exception())

        messages = get_flashed_messages(with_categories=True)
        assert messages == [("error", "Authentication with GitHub failed. Please try again.")]