"""Document upload and management routes."""

import logging

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import NotFound

from models.application import Application
from models.document import Document
from services.database import db
from utils.helpers import delete_file, save_upload

logger = logging.getLogger(__name__)

documents_bp = Blueprint("documents", __name__)


@documents_bp.route("/documents")
@login_required
def list_documents():
    """List all uploaded documents."""
    doc_type = request.args.get("type", "").strip()

    query = Document.query.filter_by(user_id=current_user.id)
    if doc_type:
        query = query.filter(Document.document_type == doc_type)

    documents = query.order_by(Document.upload_date.desc()).all()
    applications = Application.query.filter_by(user_id=current_user.id).all()

    resumes = [d for d in documents if d.document_type == "resume"]
    cover_letters = [d for d in documents if d.document_type == "cover_letter"]

    return render_template(
        "documents.html",
        documents=documents,
        resumes=resumes,
        cover_letters=cover_letters,
        applications=applications,
    )


@documents_bp.route("/documents/upload", methods=["POST"])
@login_required
def upload_document():
    """Upload a resume or cover letter."""
    if "file" not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for("documents.list_documents"))

    file = request.files["file"]
    doc_type = request.form.get("document_type", "resume")
    application_id = request.form.get("application_id", type=int)

    if doc_type not in Document.VALID_TYPES:
        flash("Invalid document type.", "error")
        return redirect(url_for("documents.list_documents"))

    if application_id:
        Application.query.filter_by(
            id=application_id, user_id=current_user.id
        ).first_or_404()

    result = save_upload(file, current_user.id)
    if not result:
        flash("Invalid file. Only PDF and DOCX files up to 10MB are allowed.", "error")
        return redirect(url_for("documents.list_documents"))

    stored_name, filepath = result

    document = Document(
        user_id=current_user.id,
        application_id=application_id,
        filename=stored_name,
        original_filename=file.filename,
        document_type=doc_type,
        filepath=filepath,
    )

    db.session.add(document)
    db.session.commit()
    logger.info("Document uploaded: %s by user %s", stored_name, current_user.id)
    flash("Document uploaded successfully!", "success")
    return redirect(url_for("documents.list_documents"))


@documents_bp.route("/documents/<int:doc_id>/download")
@login_required
def download_document(doc_id: int):
    """Download a document."""
    document = Document.query.filter_by(
        id=doc_id, user_id=current_user.id
    ).first_or_404()

    try:
        return send_file(
            document.filepath,
            as_attachment=True,
            download_name=document.original_filename,
        )
    except FileNotFoundError:
        logger.error("File not found for document %s: %s", doc_id, document.filepath)
        flash("File not found on server.", "error")
        raise NotFound()


@documents_bp.route("/documents/<int:doc_id>/delete", methods=["POST"])
@login_required
def delete_document(doc_id: int):
    """Delete a document."""
    document = Document.query.filter_by(
        id=doc_id, user_id=current_user.id
    ).first_or_404()

    delete_file(document.filepath)
    db.session.delete(document)
    db.session.commit()
    logger.info("Document deleted: %s", doc_id)
    flash("Document deleted.", "success")
    return redirect(url_for("documents.list_documents"))
