from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date

@login_required
@login_required
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    
    context = {
        'total': jobs.count(),
        'applied': jobs.filter(status='applied').count(),
        'interviews': jobs.filter(status='interview').count(),
        'offers': jobs.filter(status='offer').count(),
        'rejected': jobs.filter(status='rejected').count(),
        'withdrawn': jobs.filter(status='withdrawn').count(),
        'recent_jobs': jobs[:5],
    }
    return render(request, 'jobs/dashboard.html', context)

@login_required
def job_list(request):
    jobs = JobApplication.objects.filter(user=request.user)
    
    status = request.GET.get('status')
    if status:
        jobs = jobs.filter(status=status)
    
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_add(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # assign to logged-in user
            job.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

@login_required
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="job_applications.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Job Application Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 6))

# Add user info
    user_info = Paragraph(
    f"Generated for: {request.user.username} | Date: {date.today().strftime('%B %d, %Y')}",
    styles['Normal']
)
    elements.append(user_info)
    elements.append(Spacer(1, 12))

    jobs = JobApplication.objects.filter(user=request.user)  # only user's jobs
    
    stats_text = f"""
        Total Applications: {jobs.count()} | 
        Interviews: {jobs.filter(status='interview').count()} | 
        Offers: {jobs.filter(status='offer').count()} | 
        Rejected: {jobs.filter(status='rejected').count()}
    """
    stats = Paragraph(stats_text, styles['Normal'])
    elements.append(stats)
    elements.append(Spacer(1, 20))

    data = [['Company', 'Job Title', 'Status', 'Location', 'Remote', 'Date Applied']]

    for job in jobs:
        data.append([
            job.company_name,
            job.job_title,
            job.get_status_display(),
            job.location or 'N/A',
            'Yes' if job.is_remote else 'No',
            str(job.date_applied),
        ])

    table = Table(data, colWidths=[100, 130, 70, 90, 50, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
            [colors.white, colors.HexColor('#F3F4F6')]),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2563EB')),
    ]))

    elements.append(table)
    doc.build(elements)
    return response

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')