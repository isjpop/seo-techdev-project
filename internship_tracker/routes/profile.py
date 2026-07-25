"""User profile routes."""

import logging

from flask import Blueprint, render_template
from flask_login import current_user, login_required

logger = logging.getLogger(__name__)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def index():
    """Display user profile with GitHub and LinkedIn data."""
    github_data = current_user.get_github_data()
    linkedin_data = current_user.get_linkedin_data()

    return render_template(
        "profile.html",
        user=current_user,
        github_data=github_data,
        linkedin_data=linkedin_data,
    )
