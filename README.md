# 🎯 Job Application Tracker

A full-stack web application to track job applications during your job search, built with Django, FastAPI, Celery, and Docker.

## 🛠️ Tech Stack
- **Django** — Web framework
- **PostgreSQL** — Database (Docker)
- **FastAPI** — REST API layer
- **Celery + Redis** — Background tasks
- **ReportLab** — PDF export
- **Chart.js** — Data visualization
- **Docker** — Containerization
- **Tailwind CSS** — Styling

## ✨ Features
- Add, edit, delete job applications
- Dashboard with visual stats and doughnut chart
- Filter applications by status
- Export applications to PDF report
- REST API with auto-generated Swagger docs
- Automated daily email summary via Celery Beat

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker Desktop

### Installation

1. Clone the repo
\`\`\`bash
git clone https://github.com/Helenyixuanwang/job-tracker.git
cd job-tracker
\`\`\`

2. Create virtual environment
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

3. Create `.env` file in root folder
\`\`\`
SECRET_KEY=your_django_secret_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DB_NAME=jobtracker
DB_USER=your_db_user
DB_PASSWORD=your_db_password
\`\`\`

4. Start Docker containers
\`\`\`bash
docker-compose up -d
\`\`\`

5. Run migrations
\`\`\`bash
python manage.py migrate
\`\`\`

6. Create superuser
\`\`\`bash
python manage.py createsuperuser
\`\`\`

7. Start all services (each in separate terminal tab)
\`\`\`bash
# Tab 1 - Django
python manage.py runserver

# Tab 2 - FastAPI
uvicorn fastapi_app:app --reload --port 8001

# Tab 3 - Celery Worker
celery -A jobtracker worker --loglevel=info

# Tab 4 - Celery Beat
celery -A jobtracker beat --loglevel=info
\`\`\`

## 📡 API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/api/jobs` | GET | Get all jobs |
| `/api/jobs/{id}` | GET | Get single job |
| `/api/jobs/status/{status}` | GET | Filter by status |
| `/api/stats` | GET | Get summary stats |
| `/docs` | GET | Swagger UI docs |

## 📸 Screenshots
### Dashboard
![Dashboard](screenshots/dashboard.png)

### Job List
![Job List](screenshots/job_list.png)

### PDF Export
![PDF Export](screenshots/pdf_export.png)

## 🔧 Daily Email Summary
Celery Beat automatically sends a daily summary email at 9am with your application stats.

