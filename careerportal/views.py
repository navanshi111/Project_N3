from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Applicant, Employee, Company

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
                    company = Company.objects.create(
                        name=form.cleaned_data["new_company"])
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
        'employee': employee,
    })

def home(request):
    return render(request, 'careerportal/home.html')

# Source: https://docs.djangoproject.com/en/5.2/intro/tutorial03/
# Source: Lecture 5 (Properties)