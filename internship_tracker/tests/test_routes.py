"""Route accessibility tests."""


def test_404_page(client):
    """Unknown routes should return 404."""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404


def test_dashboard_loads(auth_client):
    """Dashboard should load for authenticated users."""
    client, _ = auth_client
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_profile_page(auth_client):
    """Profile page should display user information."""
    client, user = auth_client
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Test User" in response.data
