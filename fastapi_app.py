import sys
import os

# This lets FastAPI access your Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobtracker.settings')

import django
django.setup()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from jobs.models import JobApplication

app = FastAPI(title="Job Tracker API", version="1.0.0")

# This defines what our API response looks like
class JobSchema(BaseModel):
    id: int
    company_name: str
    job_title: str
    status: str
    location: str
    is_remote: bool
    requires_sponsorship: bool
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: str

    class Config:
        from_attributes = True

# GET all jobs
@app.get("/api/jobs", response_model=List[JobSchema])
def get_jobs():
    jobs = JobApplication.objects.all()
    return list(jobs)

# GET jobs by status
@app.get("/api/jobs/status/{status}", response_model=List[JobSchema])
def get_jobs_by_status(status: str):
    jobs = JobApplication.objects.filter(status=status)
    return list(jobs)

# GET single job
@app.get("/api/jobs/{job_id}", response_model=JobSchema)
def get_job(job_id: int):
    job = JobApplication.objects.get(id=job_id)
    return job

# GET stats summary
@app.get("/api/stats")
def get_stats():
    jobs = JobApplication.objects.all()
    return {
        "total": jobs.count(),
        "applied": jobs.filter(status="applied").count(),
        "interviews": jobs.filter(status="interview").count(),
        "offers": jobs.filter(status="offer").count(),
        "rejected": jobs.filter(status="rejected").count(),
        "withdrawn": jobs.filter(status="withdrawn").count(),
    }