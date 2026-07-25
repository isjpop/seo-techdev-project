"""File upload tests."""

import io
import os


def test_upload_valid_pdf(auth_client):
    """User should be able to upload a valid PDF file."""
    client, user = auth_client

    data = {
        "document_type": "resume",
        "file": (io.BytesIO(b"%PDF-1.4 test content"), "resume.pdf"),
    }

    response = client.post(
        "/documents/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"uploaded successfully" in response.data.lower() or b"Resume" in response.data


def test_upload_invalid_extension(auth_client):
    """Upload should reject disallowed file extensions."""
    client, user = auth_client

    data = {
        "document_type": "resume",
        "file": (io.BytesIO(b"malicious content"), "virus.exe"),
    }

    response = client.post(
        "/documents/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid file" in response.data or b"PDF" in response.data


def test_documents_page_requires_auth(client):
    """Documents page should require authentication."""
    response = client.get("/documents", follow_redirects=False)
    assert response.status_code == 302
