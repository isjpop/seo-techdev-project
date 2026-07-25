"""Interview model."""

from datetime import datetime, timezone

from services.database import db


class Interview(db.Model):
    """Interview record linked to an application."""

    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(100), nullable=False, default="Phone Screen")
    location = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    application = db.relationship("Application", back_populates="interviews")

    VALID_TYPES = [
        "Phone Screen",
        "Technical",
        "Behavioral",
        "Onsite",
        "Final Round",
        "Other",
    ]

    def __repr__(self) -> str:
        return f"<Interview {self.type} for app {self.application_id}>"
