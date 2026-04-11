from django.db import models
from django.contrib.auth.models import User

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    job_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )
    date_applied = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    is_remote = models.BooleanField(default=False)
    requires_sponsorship = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta:
        ordering = ['-date_applied']