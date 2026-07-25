"""Application model for internship tracking."""

from datetime import datetime, timezone

from services.database import db


class Application(db.Model):
    """Internship application record."""

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.String(100), nullable=True)
    application_date = db.Column(db.Date, nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Applied")
    job_link = db.Column(db.String(512), nullable=True)
    recruiter_name = db.Column(db.String(255), nullable=True)
    recruiter_email = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = db.relationship("User", back_populates="applications")
    interviews = db.relationship(
        "Interview", back_populates="application", cascade="all, delete-orphan"
    )

    VALID_STATUSES = [
        "Applied",
        "Under Review",
        "Phone Screen",
        "Interview",
        "Offer",
        "Rejected",
        "Withdrawn",
    ]

    def __repr__(self) -> str:
        return f"<Application {self.company_name} - {self.position}>"
