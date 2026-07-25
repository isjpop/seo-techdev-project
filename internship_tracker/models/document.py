"""Document model for resumes and cover letters."""

from datetime import datetime, timezone

from services.database import db


class Document(db.Model):
    """Uploaded document (resume or cover letter)."""

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True
    )
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    upload_date = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user = db.relationship("User", back_populates="documents")
    application = db.relationship("Application", backref="documents")

    VALID_TYPES = ["resume", "cover_letter"]

    def __repr__(self) -> str:
        return f"<Document {self.original_filename} ({self.document_type})>"
