from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Applicant, Employee, Company, Job, Application 


# Company
admin.site.register(Company)

#Job
admin.site.register(Job)

# Applicant Admin
@admin.register(Applicant)
class ApplicantAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Applicant Info", {"fields": ("bio", "summary")}),)

# Employee Admin
@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Employee Info", {"fields": ("company",)}),)
    
 # Application Admin 
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'created_at']
