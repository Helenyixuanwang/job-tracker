# 🎯 Job Application Tracker


[![CI](https://github.com/Helenyixuanwang/job-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Helenyixuanwang/job-tracker/actions/workflows/ci.yml)

🌐 **Live Demo:** https://job-tracker-production-4f92.up.railway.app

A full-stack job application tracking web app built with Django, FastAPI, Celery, Redis, PostgreSQL, and Docker. Designed to help job seekers organize and monitor their applications during the job search process.

## 🔄 CI/CD Pipeline
git push origin main
→ GitHub Actions: Python 3.12 + pip install + syntax check + Django system check
→ if ✅ → Railway auto-deploys to production

## 🛠️ Tech Stack
- **Django** — Web framework
- **PostgreSQL** — Database (Docker locally, Railway in production)
- **FastAPI** — REST API layer with auto-generated Swagger docs
- **Celery + Redis** — Background tasks and scheduling
- **ReportLab** — PDF report generation
- **Chart.js** — Data visualization
- **Docker** — Local containerization
- **Tailwind CSS** — Styling
- **Railway** — Cloud deployment
- **GitHub Actions** — CI/CD

## ✨ Features
- 🔐 User authentication — register, login, logout
- 👤 User-specific data — each user sees only their own jobs
- ➕ Add, edit, delete job applications
- 📊 Dashboard with visual stats and doughnut chart
- 🔍 Filter applications by status (Applied, Interview, Offer, Rejected)
- 📄 Export personalized PDF report with username and date
- 🔗 REST API with auto-generated Swagger docs
- ⏰ Automated daily personalized email summary via Celery Beat
- 🐳 Docker containerized PostgreSQL and Redis
- 🚀 Deployed on Railway with PostgreSQL and Redis

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
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
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

## 🔧 Architecture
\`\`\`
Browser  →  Django (port 8000)  →  PostgreSQL
                    ↓
              FastAPI (port 8001) →  Swagger UI
                    ↓
         Celery + Redis  →  Daily Email Summary
\`\`\`

## 📧 Daily Email Summary
Celery Beat automatically sends a daily summary email at 9am with your application stats including total applications, interviews, offers, and rejections.

## 👩‍💻 Author
Built by **Helen Wang**
- 🔗 [GitHub](https://github.com/Helenyixuanwang)
- 💼 [LinkedIn](https://www.linkedin.com/in/helenyixuanwang/)

