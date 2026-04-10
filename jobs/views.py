from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication
from .forms import JobApplicationForm

def dashboard(request):
    jobs = JobApplication.objects.all()
    
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

def job_list(request):
    jobs = JobApplication.objects.all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        jobs = jobs.filter(status=status)
    
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_add(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/job_form.html', {'form': form})

def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

def export_pdf(request):
    # Create HTTP response with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="job_applications.pdf"'

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Job Application Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Stats summary
    jobs = JobApplication.objects.all()
    stats_text = f"""
        Total Applications: {jobs.count()} | 
        Interviews: {jobs.filter(status='interview').count()} | 
        Offers: {jobs.filter(status='offer').count()} | 
        Rejected: {jobs.filter(status='rejected').count()}
    """
    stats = Paragraph(stats_text, styles['Normal'])
    elements.append(stats)
    elements.append(Spacer(1, 20))

    # Table header
    data = [['Company', 'Job Title', 'Status', 'Location', 'Remote', 'Date Applied']]

    # Table rows
    for job in jobs:
        data.append([
            job.company_name,
            job.job_title,
            job.get_status_display(),
            job.location or 'N/A',
            'Yes' if job.is_remote else 'No',
            str(job.date_applied),
        ])

    # Create and style the table
    table = Table(data, colWidths=[100, 130, 70, 90, 50, 80])
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),

        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
            [colors.white, colors.HexColor('#F3F4F6')]),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),

        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2563EB')),
    ]))

    elements.append(table)
    doc.build(elements)
    return response