from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import JobApplication

@shared_task
def send_daily_summary():
    jobs = JobApplication.objects.all()
    
    total = jobs.count()
    applied = jobs.filter(status='applied').count()
    interviews = jobs.filter(status='interview').count()
    offers = jobs.filter(status='offer').count()
    rejected = jobs.filter(status='rejected').count()

    subject = '📋 Your Daily Job Application Summary'
    message = f"""
Good morning Helen! 👋

Here is your daily job application summary:

📊 OVERVIEW
─────────────────────
Total Applications : {total}
Applied            : {applied}
Interviews         : {interviews}
Offers             : {offers}
Rejected           : {rejected}

💪 Keep going — the right job is coming!

Job Tracker App
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.SUMMARY_EMAIL],
        fail_silently=False,
    )
    
    return f"Daily summary sent! Total jobs: {total}"