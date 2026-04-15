from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Applicant(User):
    bio = models.TextField(null=True)
    summary = models.TextField(null=True)

    def clean(self):
        if not self.bio or not self.summary:
            raise ValidationError("Applicant must have both bio and summary.")

        # Preventing same user being both Applicant and Employee
        if Employee.objects.filter(username=self.username).exists():
            raise ValidationError("This user is already registered as an Employee.")

    class Meta:
        verbose_name = "applicant"

class Employee(User):
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True)

    def clean(self):
        if not self.company:
            raise ValidationError("Employee must be assigned to a company.")

        # Preventing same user being both Employee and Applicant
        if Applicant.objects.filter(username=self.username).exists():
            raise ValidationError("This user is already registered as an Applicant.")

    class Meta:
        verbose_name = "employee"

# Source is https://docs.djangoproject.com/en/5.2/intro/tutorial02/
# Source = Jan
#starting jobs: (also sourced from django2tutorials)
#class Job(models.Model):
    #title = models.CharField(max_length=200)
    #description = models.TextField()
    #company = models.ForeignKey("Company", on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField(default='2026-12-31')  # temporary default
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title