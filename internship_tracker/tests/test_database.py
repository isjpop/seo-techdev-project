"""Database model tests."""

from datetime import date, datetime, timezone

from models.application import Application
from models.document import Document
from models.interview import Interview
from models.user import User
from services.database import db


def test_user_creation(app):
    """User model should persist correctly."""
    with app.app_context():
        user = User(name="Jane Doe", email="jane@example.com", github_id="janedoe")
        db.session.add(user)
        db.session.commit()

        fetched = User.query.filter_by(email="jane@example.com").first()
        assert fetched is not None
        assert fetched.name == "Jane Doe"
        assert fetched.github_id == "janedoe"


def test_cascade_delete(app):
    """Deleting a user should cascade to applications and interviews."""
    with app.app_context():
        user = User(name="Bob", email="bob@example.com")
        db.session.add(user)
        db.session.commit()

        application = Application(
            user_id=user.id,
            company_name="Google",
            position="SWE Intern",
            status="Applied",
        )
        db.session.add(application)
        db.session.commit()

        interview = Interview(
            application_id=application.id,
            date=datetime.now(timezone.utc),
            type="Phone Screen",
        )
        db.session.add(interview)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        assert Application.query.count() == 0
        assert Interview.query.count() == 0


def test_github_data_storage(app):
    """User should store and retrieve GitHub data as JSON."""
    with app.app_context():
        user = User(name="Dev", email="dev@example.com")
        user.set_github_data({"username": "devuser", "repo_count": 5})
        db.session.add(user)
        db.session.commit()

        data = user.get_github_data()
        assert data["username"] == "devuser"
        assert data["repo_count"] == 5
