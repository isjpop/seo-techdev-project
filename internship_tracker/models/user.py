"""User model."""

import json
from datetime import datetime, timezone

from flask_login import UserMixin

from services.database import db


class User(UserMixin, db.Model):
    """Application user authenticated via OAuth."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    github_id = db.Column(db.String(64), unique=True, nullable=True, index=True)
    linkedin_id = db.Column(db.String(64), unique=True, nullable=True, index=True)
    profile_picture = db.Column(db.String(512), nullable=True)
    github_username = db.Column(db.String(255), nullable=True)
    github_data = db.Column(db.Text, nullable=True)
    linkedin_data = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    applications = db.relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )
    documents = db.relationship(
        "Document", back_populates="user", cascade="all, delete-orphan"
    )

    def set_github_data(self, data: dict) -> None:
        """Store GitHub profile data as JSON."""
        self.github_data = json.dumps(data)

    def get_github_data(self) -> dict:
        """Retrieve GitHub profile data."""
        if not self.github_data:
            return {}
        return json.loads(self.github_data)

    def set_linkedin_data(self, data: dict) -> None:
        """Store LinkedIn profile data as JSON."""
        self.linkedin_data = json.dumps(data)

    def get_linkedin_data(self) -> dict:
        """Retrieve LinkedIn profile data."""
        if not self.linkedin_data:
            return {}
        return json.loads(self.linkedin_data)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
