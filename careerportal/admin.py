from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, Job, Applicant, Employee, Application, SavedJob

# Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)

#Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'job_type', 'required_degree', 'deadline')
    list_filter = ('job_type', 'required_degree', 'pay_status')
    search_fields = ('title', 'description')

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
    list_display = ('applicant', 'job', 'status', 'created_at')
    list_filter = ('status', 'created_at')

# Saved Job Admin
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'saved_at']