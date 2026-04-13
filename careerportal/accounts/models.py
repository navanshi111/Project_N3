from django.contrib.auth.models import AbstractUser
from django.db import models

# Source is https://docs.djangoproject.com/en/5.2/intro/tutorial02/

class User(AbstractUser): # Using AbstractUser so everything (user + userprofile) is in one model.
    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# company = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True)
