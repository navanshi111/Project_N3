from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

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
    DEGREE_CHOICES = [
        ("high_school", "High School Diploma"),
        ("bachelors", "Bachelor's Degree"),
        ("masters", "Master's Degree"),
        ("phD", "PhD"),
        ("post_doc", "Post-Doctorate")
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    ]
    PAY_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    contact_info = models.TextField(
        help_text="Include contact email, phone, and/or company website link.",
        blank=True,
        default=''
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    required_degree = models.CharField(
        max_length=50,
        choices=DEGREE_CHOICES,
        default="bachelors"
    )
    deadline = models.DateField(default=date.today) # temporary default
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True
    )
    
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full_time'
    )
    pay_status = models.CharField(
        max_length=10,
        choices=PAY_CHOICES,
        default='paid'
    )

    def __str__(self):
        return self.title
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    text = models.TextField()
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class SavedJob(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('applicant', 'job')

    def __str__(self):
        return f"{self.applicant.username} saved {self.job.title}"