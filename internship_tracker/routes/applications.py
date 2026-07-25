"""Application CRUD routes."""

import logging

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models.application import Application
from models.interview import Interview
from services.database import db
from sqlalchemy import or_
from utils.helpers import paginate_query
from utils.validators import parse_date, parse_datetime, validate_application_data

logger = logging.getLogger(__name__)

applications_bp = Blueprint("applications", __name__)


@applications_bp.route("/applications")
@login_required
def list_applications():
    """List applications with search, filter, sort, and pagination."""
    query = Application.query.filter_by(user_id=current_user.id)

    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()
    sort_by = request.args.get("sort", "created_at")
    sort_dir = request.args.get("dir", "desc")
    page = request.args.get("page", 1, type=int)

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                Application.company_name.ilike(like),
                Application.position.ilike(like),
                Application.location.ilike(like),
                Application.recruiter_name.ilike(like),
            )
        )

    if status_filter:
        query = query.filter(Application.status == status_filter)

    sort_column = getattr(Application, sort_by, Application.created_at)
    if sort_dir == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    pagination = paginate_query(query, page)
    statuses = Application.VALID_STATUSES

    return render_template(
        "applications.html",
        applications=pagination.items,
        pagination=pagination,
        search=search,
        status_filter=status_filter,
        sort_by=sort_by,
        sort_dir=sort_dir,
        statuses=statuses,
    )


@applications_bp.route("/applications/new", methods=["GET", "POST"])
@login_required
def create_application():
    """Create a new internship application."""
    if request.method == "POST":
        data = {
            "company_name": request.form.get("company_name", ""),
            "position": request.form.get("position", ""),
            "location": request.form.get("location", ""),
            "salary": request.form.get("salary", ""),
            "application_date": request.form.get("application_date", ""),
            "deadline": request.form.get("deadline", ""),
            "status": request.form.get("status", "Applied"),
            "job_link": request.form.get("job_link", ""),
            "recruiter_name": request.form.get("recruiter_name", ""),
            "recruiter_email": request.form.get("recruiter_email", ""),
            "notes": request.form.get("notes", ""),
        }

        valid, errors = validate_application_data(data)
        if not valid:
            for error in errors:
                flash(error, "error")
            return render_template("application_form.html", application=None, data=data)

        duplicate = Application.query.filter_by(
            user_id=current_user.id,
            company_name=data["company_name"].strip(),
            position=data["position"].strip(),
        ).first()

        if duplicate:
            flash("An application for this company and position already exists.", "error")
            return render_template("application_form.html", application=None, data=data)

        app_record = Application(
            user_id=current_user.id,
            company_name=data["company_name"].strip(),
            position=data["position"].strip(),
            location=data.get("location", "").strip() or None,
            salary=data.get("salary", "").strip() or None,
            application_date=parse_date(data.get("application_date", "")),
            deadline=parse_date(data.get("deadline", "")),
            status=data.get("status", "Applied"),
            job_link=data.get("job_link", "").strip() or None,
            recruiter_name=data.get("recruiter_name", "").strip() or None,
            recruiter_email=data.get("recruiter_email", "").strip() or None,
            notes=data.get("notes", "").strip() or None,
        )

        db.session.add(app_record)
        db.session.commit()
        logger.info("Created application %s for user %s", app_record.id, current_user.id)
        flash("Application created successfully!", "success")
        return redirect(url_for("applications.detail", app_id=app_record.id))

    return render_template("application_form.html", application=None, data={})


@applications_bp.route("/applications/<int:app_id>")
@login_required
def detail(app_id: int):
    """View application details."""
    app_record = Application.query.filter_by(
        id=app_id, user_id=current_user.id
    ).first_or_404()

    interviews = (
        Interview.query.filter_by(application_id=app_id)
        .order_by(Interview.date.desc())
        .all()
    )

    return render_template(
        "application_detail.html",
        application=app_record,
        interviews=interviews,
        interview_types=Interview.VALID_TYPES,
    )


@applications_bp.route("/applications/<int:app_id>/edit", methods=["GET", "POST"])
@login_required
def edit_application(app_id: int):
    """Edit an existing application."""
    app_record = Application.query.filter_by(
        id=app_id, user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        data = {
            "company_name": request.form.get("company_name", ""),
            "position": request.form.get("position", ""),
            "location": request.form.get("location", ""),
            "salary": request.form.get("salary", ""),
            "application_date": request.form.get("application_date", ""),
            "deadline": request.form.get("deadline", ""),
            "status": request.form.get("status", "Applied"),
            "job_link": request.form.get("job_link", ""),
            "recruiter_name": request.form.get("recruiter_name", ""),
            "recruiter_email": request.form.get("recruiter_email", ""),
            "notes": request.form.get("notes", ""),
        }

        valid, errors = validate_application_data(data)
        if not valid:
            for error in errors:
                flash(error, "error")
            return render_template("application_form.html", application=app_record, data=data)

        app_record.company_name = data["company_name"].strip()
        app_record.position = data["position"].strip()
        app_record.location = data.get("location", "").strip() or None
        app_record.salary = data.get("salary", "").strip() or None
        app_record.application_date = parse_date(data.get("application_date", ""))
        app_record.deadline = parse_date(data.get("deadline", ""))
        app_record.status = data.get("status", "Applied")
        app_record.job_link = data.get("job_link", "").strip() or None
        app_record.recruiter_name = data.get("recruiter_name", "").strip() or None
        app_record.recruiter_email = data.get("recruiter_email", "").strip() or None
        app_record.notes = data.get("notes", "").strip() or None

        db.session.commit()
        logger.info("Updated application %s", app_id)
        flash("Application updated successfully!", "success")
        return redirect(url_for("applications.detail", app_id=app_id))

    data = {
        "company_name": app_record.company_name,
        "position": app_record.position,
        "location": app_record.location or "",
        "salary": app_record.salary or "",
        "application_date": app_record.application_date.isoformat() if app_record.application_date else "",
        "deadline": app_record.deadline.isoformat() if app_record.deadline else "",
        "status": app_record.status,
        "job_link": app_record.job_link or "",
        "recruiter_name": app_record.recruiter_name or "",
        "recruiter_email": app_record.recruiter_email or "",
        "notes": app_record.notes or "",
    }
    return render_template("application_form.html", application=app_record, data=data)


@applications_bp.route("/applications/<int:app_id>/delete", methods=["POST"])
@login_required
def delete_application(app_id: int):
    """Delete an application."""
    app_record = Application.query.filter_by(
        id=app_id, user_id=current_user.id
    ).first_or_404()

    db.session.delete(app_record)
    db.session.commit()
    logger.info("Deleted application %s", app_id)
    flash("Application deleted.", "success")
    return redirect(url_for("applications.list_applications"))


@applications_bp.route("/applications/<int:app_id>/interviews", methods=["POST"])
@login_required
def add_interview(app_id: int):
    """Add an interview to an application."""
    Application.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()

    interview_date = parse_datetime(request.form.get("date", ""))
    if not interview_date:
        flash("Invalid interview date.", "error")
        return redirect(url_for("applications.detail", app_id=app_id))

    interview = Interview(
        application_id=app_id,
        date=interview_date,
        type=request.form.get("type", "Phone Screen"),
        location=request.form.get("location", "").strip() or None,
        notes=request.form.get("notes", "").strip() or None,
    )

    db.session.add(interview)
    db.session.commit()
    logger.info("Added interview to application %s", app_id)
    flash("Interview added!", "success")
    return redirect(url_for("applications.detail", app_id=app_id))


@applications_bp.route("/applications/<int:app_id>/interviews/<int:interview_id>/delete", methods=["POST"])
@login_required
def delete_interview(app_id: int, interview_id: int):
    """Delete an interview."""
    Application.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()
    interview = Interview.query.filter_by(id=interview_id, application_id=app_id).first_or_404()

    db.session.delete(interview)
    db.session.commit()
    flash("Interview removed.", "success")
    return redirect(url_for("applications.detail", app_id=app_id))


@applications_bp.route("/api/applications/search")
@login_required
def api_search():
    """AJAX search endpoint for applications."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    results = (
        Application.query.filter_by(user_id=current_user.id)
        .filter(
            or_(
                Application.company_name.ilike(f"%{q}%"),
                Application.position.ilike(f"%{q}%"),
            )
        )
        .limit(10)
        .all()
    )

    return jsonify([
        {
            "id": a.id,
            "company_name": a.company_name,
            "position": a.position,
            "status": a.status,
        }
        for a in results
    ])
