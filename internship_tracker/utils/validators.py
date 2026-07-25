"""Input validation utilities."""

import re
from datetime import date, datetime
from typing import Optional
from urllib.parse import urlparse


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not url:
        return True
    try:
        result = urlparse(url.strip())
        return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
        return False


def parse_date(value: str) -> Optional[date]:
    """Parse a date string in YYYY-MM-DD format."""
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_datetime(value: str) -> Optional[datetime]:
    """Parse a datetime string in ISO format."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        return None


def validate_required_fields(data: dict, fields: list[str]) -> list[str]:
    """Return list of missing required field names."""
    missing = []
    for field in fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


def validate_application_data(data: dict) -> tuple[bool, list[str]]:
    """Validate application form data."""
    errors = []

    missing = validate_required_fields(data, ["company_name", "position"])
    if missing:
        errors.extend(f"{f.replace('_', ' ').title()} is required." for f in missing)

    if data.get("recruiter_email") and not validate_email(data["recruiter_email"]):
        errors.append("Invalid recruiter email format.")

    if data.get("job_link") and not validate_url(data["job_link"]):
        errors.append("Invalid job link URL.")

    if data.get("application_date"):
        if parse_date(data["application_date"]) is None:
            errors.append("Invalid application date format.")

    if data.get("deadline"):
        if parse_date(data["deadline"]) is None:
            errors.append("Invalid deadline date format.")

    status = data.get("status", "Applied")
    from models.application import Application

    if status not in Application.VALID_STATUSES:
        errors.append(f"Invalid status. Must be one of: {', '.join(Application.VALID_STATUSES)}")

    return len(errors) == 0, errors
