"""Helper utilities."""

import logging
import os
import uuid
from pathlib import Path
from typing import Optional

from flask import current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file, user_id: int) -> Optional[tuple[str, str]]:
    """
    Save an uploaded file securely.

    Returns:
        Tuple of (stored_filename, filepath) or None on failure.
    """
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename):
        logger.warning("Rejected upload with disallowed extension: %s", file.filename)
        return None

    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[1].lower()
    stored_name = f"{user_id}_{uuid.uuid4().hex}.{ext}"

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    filepath = upload_dir / stored_name
    file.save(str(filepath))
    logger.info("Saved upload: %s -> %s", original, filepath)
    return stored_name, str(filepath)


def delete_file(filepath: str) -> bool:
    """Delete a file from disk."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info("Deleted file: %s", filepath)
            return True
    except OSError as exc:
        logger.error("Failed to delete file %s: %s", filepath, exc)
    return False


def paginate_query(query, page: int, per_page: int = 10):
    """Paginate a SQLAlchemy query."""
    page = max(1, page)
    per_page = min(max(1, per_page), 50)
    return query.paginate(page=page, per_page=per_page, error_out=False)
