"""Dashboard routes."""

import logging
from collections import Counter
from datetime import date, datetime, timedelta, timezone

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from models.application import Application
from models.interview import Interview
from services.database import db

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    """Render dashboard with statistics and charts."""
    user_id = current_user.id
    applications = Application.query.filter_by(user_id=user_id).all()

    total = len(applications)
    interviews_scheduled = Interview.query.join(Application).filter(
        Application.user_id == user_id,
        Interview.date >= datetime.now(timezone.utc),
    ).count()

    offers = sum(1 for a in applications if a.status == "Offer")
    rejections = sum(1 for a in applications if a.status == "Rejected")

    responded = sum(
        1 for a in applications if a.status not in ("Applied", "Under Review")
    )
    response_rate = round((responded / total * 100), 1) if total > 0 else 0

    stats = {
        "total_applications": total,
        "interviews_scheduled": interviews_scheduled,
        "offers": offers,
        "rejections": rejections,
        "response_rate": response_rate,
    }

    recent_applications = (
        Application.query.filter_by(user_id=user_id)
        .order_by(Application.created_at.desc())
        .limit(5)
        .all()
    )

    today = date.today()
    upcoming_deadlines = (
        Application.query.filter_by(user_id=user_id)
        .filter(Application.deadline >= today)
        .order_by(Application.deadline.asc())
        .limit(5)
        .all()
    )

    upcoming_interviews = (
        Interview.query.join(Application)
        .filter(
            Application.user_id == user_id,
            Interview.date >= datetime.now(timezone.utc),
        )
        .order_by(Interview.date.asc())
        .limit(5)
        .all()
    )

    recent_recruiters = (
        Application.query.filter_by(user_id=user_id)
        .filter(Application.recruiter_name.isnot(None))
        .order_by(Application.updated_at.desc())
        .limit(5)
        .all()
    )

    status_counts = Counter(a.status for a in applications)
    status_labels = list(status_counts.keys()) or ["No Data"]
    status_values = list(status_counts.values()) or [0]

    six_months_ago = today.replace(day=1) - timedelta(days=150)
    monthly_data = (
        db.session.query(
            func.strftime("%Y-%m", Application.application_date).label("month"),
            func.count(Application.id).label("count"),
        )
        .filter(
            Application.user_id == user_id,
            Application.application_date.isnot(None),
            Application.application_date >= six_months_ago,
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    month_labels = [row.month for row in monthly_data] or ["No Data"]
    month_values = [row.count for row in monthly_data] or [0]

    interview_timeline = (
        Interview.query.join(Application)
        .filter(Application.user_id == user_id)
        .order_by(Interview.date.desc())
        .limit(10)
        .all()
    )

    logger.info("Dashboard loaded for user %s", user_id)

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_applications=recent_applications,
        upcoming_deadlines=upcoming_deadlines,
        upcoming_interviews=upcoming_interviews,
        recent_recruiters=recent_recruiters,
        status_labels=status_labels,
        status_values=status_values,
        month_labels=month_labels,
        month_values=month_values,
        interview_timeline=interview_timeline,
    )
