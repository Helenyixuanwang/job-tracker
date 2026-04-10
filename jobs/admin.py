from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'job_title', 
        'status',
        'location',
        'is_remote',
        'requires_sponsorship',
        'date_applied'
    ]
    list_filter = ['status', 'is_remote', 'requires_sponsorship']
    search_fields = ['company_name', 'job_title']