from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import JobApplication

@shared_task
def send_daily_summary():
    # Get all active users with email addresses
    users = User.objects.filter(is_active=True).exclude(email='')
    
    sent_count = 0
    
    for user in users:
        # Get this specific user's jobs
        jobs = JobApplication.objects.filter(user=user)
        
        total = jobs.count()
        
        # Skip users with no applications
        if total == 0:
            continue
        
        applied = jobs.filter(status='applied').count()
        interviews = jobs.filter(status='interview').count()
        offers = jobs.filter(status='offer').count()
        rejected = jobs.filter(status='rejected').count()

        subject = '📋 Your Daily Job Application Summary'
        message = f"""
Good morning {user.username}! 👋

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
            recipient_list=[user.email],
            fail_silently=True,
        )
        sent_count += 1
    
    return f"Daily summary sent to {sent_count} users!"