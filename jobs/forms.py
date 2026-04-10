from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'company_name',
            'job_title',
            'job_url',
            'location',
            'salary_min',
            'salary_max',
            'status',
            'is_remote',
            'requires_sponsorship',
            'notes',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'e.g. ParsonsKellogg'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'e.g. Junior Full-Stack Developer'
            }),
            'job_url': forms.URLInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'https://...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'e.g. Seattle, WA or Remote'
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'e.g. 60000'
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'e.g. 90000'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'rows': 3,
                'placeholder': 'Any notes about this job...'
            }),
        }