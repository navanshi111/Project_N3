from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Applicant, Employee, Company, Job, Application 
from .forms import RegisterForm, JobForm, ApplicationForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user_type = form.cleaned_data.get("user_type")

            if user_type == "applicant":
                user = Applicant.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],)
                user.email = form.cleaned_data.get("email")
                user.bio = form.cleaned_data["bio"]
                user.summary = form.cleaned_data["summary"]
                user.save()

            elif user_type == "employee":
                company_value = form.cleaned_data["company"]

                if company_value == "other":
                    name = form.cleaned_data["new_company"].strip()

                    company, created = Company.objects.get_or_create(
                        name__iexact=name,
                        defaults={"name": name})
                else:
                    company = Company.objects.get(id=company_value)

                user = Employee.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],)
                user.email = form.cleaned_data.get("email")
                user.company = company
                user.save()

            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'careerportal/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user

    applicant = None
    employee = None

    try:
        applicant = Applicant.objects.get(id=user.id)
    except Applicant.DoesNotExist:
        pass

    try:
        employee = Employee.objects.get(id=user.id)
    except Employee.DoesNotExist:
        pass

    return render(request, 'careerportal/profile.html', {
        'applicant': applicant,
        'employee': employee,})

def home(request):
    return render(request, 'careerportal/home.html')

# Source: https://docs.djangoproject.com/en/5.2/intro/tutorial03/

#start job

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')

    degree = request.GET.get('degree')

    if degree:
        jobs = jobs.filter(required_degree=degree)

    return render(request, "careerportal/jobs.html", 
        {"jobs": jobs,
         "degree_choices": Job.Degree_Choices,
        })

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'careerportal/job_detail.html', {'job': job})


@login_required
def post_job(request):
    try:
        employee = Employee.objects.get(id=request.user.id)
    except Employee.DoesNotExist:
        messages.error(request, "Only employees can post jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = employee
            job.save()
            messages.success(request, "Job posted successfully!")
            return HttpResponseRedirect(reverse('job_list'))
    else:
        form = JobForm()

    return render(request, 'careerportal/post_job.html', {'form': form})

# editing for applications 
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    try:
        applicant = Applicant.objects.get(id=request.user.id)
    except Applicant.DoesNotExist:
        messages.error(request, "Only applicants can apply for jobs.")
        return redirect('job_detail', job_id=job_id)

    # Prevent applying twice
    already_applied = Application.objects.filter(job=job, applicant=applicant).exists()
    if already_applied:
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = applicant
            application.save()
            messages.success(request, "Application submitted!")
            return HttpResponseRedirect(reverse('my_applications'))
    else:
        form = ApplicationForm()

    return render(request, 'careerportal/apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    try:
        applicant = Applicant.objects.get(id=request.user.id)
    except Applicant.DoesNotExist:
        messages.error(request, "This page is for applicants only.")
        return redirect('home')

    applications = Application.objects.filter(applicant=applicant).order_by('-created_at')
    return render(request, 'careerportal/my_applications.html', {
        'applications': applications
    })