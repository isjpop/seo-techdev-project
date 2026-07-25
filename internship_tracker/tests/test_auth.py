"""Authentication tests."""


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
