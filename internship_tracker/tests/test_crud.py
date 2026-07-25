"""Application CRUD route tests."""


def test_create_application(auth_client):
    """Authenticated user should be able to create an application."""
    client, user = auth_client

    response = client.post(
        "/applications/new",
        data={
            "company_name": "Meta",
            "position": "Software Engineer Intern",
            "location": "Menlo Park, CA",
            "status": "Applied",
            "application_date": "2026-01-15",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Meta" in response.data


def test_list_applications(auth_client):
    """Applications list should show user's applications."""
    client, user = auth_client

    client.post(
        "/applications/new",
        data={
            "company_name": "Apple",
            "position": "iOS Intern",
            "status": "Applied",
        },
    )

    response = client.get("/applications")
    assert response.status_code == 200
    assert b"Apple" in response.data


def test_delete_application(auth_client):
    """User should be able to delete their application."""
    client, user = auth_client

    client.post(
        "/applications/new",
        data={
            "company_name": "Netflix",
            "position": "Backend Intern",
            "status": "Applied",
        },
    )

    from models.application import Application
    from services.database import db

    with client.application.app_context():
        app_record = Application.query.filter_by(company_name="Netflix").first()
        app_id = app_record.id

    response = client.post(
        f"/applications/{app_id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with client.application.app_context():
        assert Application.query.filter_by(company_name="Netflix").first() is None
