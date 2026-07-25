"""Pytest configuration and fixtures."""

import os
import tempfile

import pytest

from app import create_app
from config import TestingConfig
from services.database import db as _db


@pytest.fixture
def app():
    """Create application for testing."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    class TestConfig(TestingConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        UPLOAD_FOLDER = tempfile.mkdtemp()

    application = create_app(TestConfig)

    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()

    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    """Authenticated test client with a logged-in user."""
    from models.user import User

    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
            github_id="testuser",
            github_username="testuser",
        )
        _db.session.add(user)
        _db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)
        sess["_fresh"] = True

    with app.app_context():
        user = _db.session.get(User, user_id)

    return client, user
