"""Flask application factory."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFError, CSRFProtect

from config import Config
from models.user import User
from routes.applications import applications_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.documents import documents_bp
from routes.profile import profile_bp
from services.database import db, init_db
from services.oauth import init_oauth

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    _setup_logging(app)
    _ensure_directories(app)

    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    csrf.init_app(app)
    init_oauth(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(profile_bp)

    _register_error_handlers(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    return app


def _setup_logging(app):
    """Configure application logging."""
    log_level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    app.logger.setLevel(log_level)


def _ensure_directories(app):
    """Create required directories."""
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    instance_dir = Path(app.instance_path)
    instance_dir.mkdir(parents=True, exist_ok=True)


def _register_error_handlers(app):
    """Register HTTP error handlers."""

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error("Internal server error: %s", error)
        return render_template("500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        app.logger.warning("CSRF validation failed: %s", error.description)
        flash("Your session expired or the form was invalid. Please try again.", "error")
        return redirect(url_for("auth.login"))


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)