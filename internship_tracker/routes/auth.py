"""Authentication routes."""

import logging

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from models.user import User
from services.database import db
from services.github_api import fetch_github_email, fetch_github_profile
from services.linkedin_api import fetch_linkedin_profile
from services.oauth import get_redirect_uri, handle_oauth_error, oauth

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
@auth_bp.route("/login")
def login():
    """Render login landing page."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("login.html")


@auth_bp.route("/auth/github")
def github_login():
    """Initiate GitHub OAuth flow."""
    redirect_uri = get_redirect_uri("github")
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route("/auth/linkedin")
def linkedin_login():
    """Initiate LinkedIn OAuth flow."""
    redirect_uri = get_redirect_uri("linkedin")
    return oauth.linkedin.authorize_redirect(redirect_uri)


@auth_bp.route("/auth/callback/github")
def github_callback():
    """Handle GitHub OAuth callback."""
    try:
        token = oauth.github.authorize_access_token()
        if not token:
            flash("GitHub authentication failed.", "error")
            return redirect(url_for("auth.login"))

        access_token = token.get("access_token")
        profile = fetch_github_profile(access_token)

        email = profile.get("email") or fetch_github_email(access_token)
        if not email:
            flash("Unable to retrieve email from GitHub. Please make your email public.", "error")
            return redirect(url_for("auth.login"))

        github_id = str(profile.get("username", ""))
        user = User.query.filter_by(github_id=github_id).first()

        if not user:
            user = User.query.filter_by(email=email).first()

        if user:
            user.name = profile["name"]
            user.email = email
            user.github_id = github_id
            user.github_username = profile["username"]
            user.profile_picture = profile.get("profile_picture") or user.profile_picture
            user.set_github_data(profile)
        else:
            user = User(
                name=profile["name"],
                email=email,
                github_id=github_id,
                github_username=profile["username"],
                profile_picture=profile.get("profile_picture"),
            )
            user.set_github_data(profile)
            db.session.add(user)

        db.session.commit()
        login_user(user)
        logger.info("User logged in via GitHub: %s", email)
        flash("Successfully logged in with GitHub!", "success")
        return redirect(url_for("dashboard.index"))

    except Exception as exc:
        return handle_oauth_error("github", exc)


@auth_bp.route("/auth/callback/linkedin")
def linkedin_callback():
    """Handle LinkedIn OAuth callback."""
    try:
        if request.args.get("error"):
            raise Exception(
                request.args.get("error_description") or request.args.get("error") or "LinkedIn OAuth error"
            )

        state = request.args.get("state")
        code = request.args.get("code")
        state_data = oauth.linkedin.framework.get_state_data(session, state)

        if not state_data:
            raise Exception("Missing or invalid OAuth state for LinkedIn callback.")

        oauth.linkedin.framework.clear_state_data(session, state)

        redirect_uri = state_data.get("redirect_uri") or get_redirect_uri("linkedin")
        token = oauth.linkedin.fetch_access_token(
            redirect_uri=redirect_uri,
            code=code,
        )
        if not token:
            flash("LinkedIn authentication failed.", "error")
            return redirect(url_for("auth.login"))

        access_token = token.get("access_token")
        profile = fetch_linkedin_profile(access_token)

        email = profile.get("email")
        linkedin_id = profile.get("sub", "")

        if not email:
            flash("Unable to retrieve email from LinkedIn.", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(linkedin_id=linkedin_id).first()

        if not user:
            user = User.query.filter_by(email=email).first()

        if user:
            user.name = profile.get("full_name") or user.name
            user.email = email
            user.linkedin_id = linkedin_id
            if profile.get("profile_picture"):
                user.profile_picture = profile["profile_picture"]
            user.set_linkedin_data(profile)
        else:
            user = User(
                name=profile.get("full_name", "LinkedIn User"),
                email=email,
                linkedin_id=linkedin_id,
                profile_picture=profile.get("profile_picture"),
            )
            user.set_linkedin_data(profile)
            db.session.add(user)

        db.session.commit()
        login_user(user)
        logger.info("User logged in via LinkedIn: %s", email)
        flash("Successfully logged in with LinkedIn!", "success")
        return redirect(url_for("dashboard.index"))

    except Exception as exc:
        return handle_oauth_error("linkedin", exc)


@auth_bp.route("/auth/connect/github")
@login_required
def connect_github():
    """Connect GitHub account to existing user."""
    redirect_uri = get_redirect_uri("github")
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route("/auth/connect/linkedin")
@login_required
def connect_linkedin():
    """Connect LinkedIn account to existing user."""
    redirect_uri = get_redirect_uri("linkedin")
    return oauth.linkedin.authorize_redirect(redirect_uri)


@auth_bp.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logger.info("User logged out: %s", current_user.email)
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
