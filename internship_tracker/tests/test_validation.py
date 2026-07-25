"""Validation utility tests."""

from utils.validators import (
    parse_date,
    validate_application_data,
    validate_email,
    validate_url,
)


def test_validate_email():
    """Email validator should accept valid and reject invalid emails."""
    assert validate_email("user@example.com") is True
    assert validate_email("user.name+tag@domain.co.uk") is True
    assert validate_email("invalid") is False
    assert validate_email("") is False
    assert validate_email("@missing.com") is False


def test_validate_url():
    """URL validator should accept valid HTTP(S) URLs."""
    assert validate_url("https://careers.google.com/jobs/123") is True
    assert validate_url("http://example.com") is True
    assert validate_url("") is True
    assert validate_url("not-a-url") is False
    assert validate_url("ftp://files.com") is False


def test_validate_application_data():
    """Application data validator should catch missing required fields."""
    valid, errors = validate_application_data({
        "company_name": "Stripe",
        "position": "SWE Intern",
        "status": "Applied",
    })
    assert valid is True
    assert errors == []

    valid, errors = validate_application_data({
        "company_name": "",
        "position": "",
    })
    assert valid is False
    assert len(errors) >= 2


def test_parse_date():
    """Date parser should handle valid and invalid formats."""
    assert parse_date("2026-03-15") is not None
    assert parse_date("2026-03-15").year == 2026
    assert parse_date("") is None
    assert parse_date("invalid") is None
