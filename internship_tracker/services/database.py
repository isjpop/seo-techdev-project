"""Database initialization and session management."""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """Initialize database with the Flask application."""
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
