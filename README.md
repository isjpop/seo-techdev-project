# Introducing our SEO Tech Developer Final Project

Created by Juan Pablo Flores Villarreal, Aqila Nasiry, and Sebastian Hernandez

## Internship Tracker

We decided on building a full-stack web internship/job application tracker for students and job seekers. Functionalities include: 
linking account to both GitHub and LinkedIn, upload and track different applications based on company, position, location, pay, etc,
storing and tracking of different resume and cover letter versions.

## Features

- **OAuth Authentication** — Sign in with GitHub or LinkedIn
- **Application Management** — Full CRUD with search, filter, sort, and pagination
- **Dashboard Analytics** — Statistics cards, status pie chart, monthly bar chart
- **Interview Tracking** — Timeline with notes, types, and locations
- **Document Management** — Upload, download, and version resumes and cover letters (PDF/DOCX)
- **Recruiter Information** — Track contacts per application
- **Profile Page** — Display GitHub repos and LinkedIn profile data

## Requirements

- Python 3.10+
- pip
- GitHub OAuth App credentials
- LinkedIn OAuth App credentials (optional but recommended)

## Installation

```bash
# Clone the repository
git clone https://github.com/isjpop/seo-techdev-project
cd internship_tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OAuth credentials
```

## Running Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

Tests cover authentication, database models, CRUD operations, validation, file uploads, and routes.

## Project Architecture

```
internship_tracker/
├── app.py                 # Application factory & entry point
├── config.py              # Configuration classes
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── models/                # SQLAlchemy models
│   ├── user.py
│   ├── application.py
│   ├── interview.py
│   └── document.py
├── routes/                # Flask blueprints
│   ├── auth.py
│   ├── dashboard.py
│   ├── applications.py
│   ├── documents.py
│   └── profile.py
├── services/              # Business logic & external APIs
│   ├── database.py
│   ├── oauth.py
│   ├── github_api.py
│   └── linkedin_api.py
├── utils/                 # Helpers & validators
│   ├── validators.py
│   └── helpers.py
├── templates/             # Jinja2 HTML templates
├── static/                # CSS & JavaScript
│   ├── css/
│   └── js/
├── tests/                 # pytest test suite
├── docs/                  # Architecture diagrams & wireframes
├── uploads/               # Uploaded documents (gitignored)
└── instance/              # SQLite database (gitignored)
```

See [docs/architecture.md](docs/architecture.md) for Mermaid diagrams and [docs/wireframes.md](docs/wireframes.md) for page wireframes.

## Database Schema

### users
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Display name |
| email | String | Unique email |
| github_id | String | GitHub username |
| linkedin_id | String | LinkedIn user ID |
| profile_picture | String | Avatar URL |
| created_at | DateTime | Account creation |

### applications
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK → users |
| company_name | String | Company name |
| position | String | Job title |
| location | String | Job location |
| salary | String | Compensation |
| application_date | Date | Date applied |
| deadline | Date | Application deadline |
| status | String | Current status |
| job_link | String | Posting URL |
| recruiter_name | String | Recruiter name |
| recruiter_email | String | Recruiter email |
| notes | Text | Application notes |

### interviews
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| application_id | Integer | FK → applications |
| date | DateTime | Interview date/time |
| type | String | Interview type |
| location | String | Location or link |
| notes | Text | Interview notes |

### documents
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK → users |
| application_id | Integer | FK → applications (optional) |
| filename | String | Stored filename |
| original_filename | String | Original upload name |
| document_type | String | resume or cover_letter |
| filepath | String | File path on disk |
| upload_date | DateTime | Upload timestamp |

## Security

- Flask-Login session management
- CSRF protection via Flask-WTF
- Environment variables for secrets
- Secure file upload validation (PDF/DOCX only, 10MB max)
- Input validation on all forms
- SQL injection prevention via SQLAlchemy ORM
- XSS protection via Jinja2 auto-escaping

## License

MIT
