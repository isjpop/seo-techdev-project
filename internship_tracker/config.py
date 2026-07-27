"""Application configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'internship_tracker.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
    LINKEDIN_CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
    LINKEDIN_SERVER_METADATA_URL = os.environ.get(
        "LINKEDIN_SERVER_METADATA_URL",
        "https://www.linkedin.com/oauth/.well-known/openid-configuration",
    )
    OAUTH_REDIRECT_BASE = os.environ.get("OAUTH_REDIRECT_BASE", "http://localhost:5000")

    # Uploads
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True
