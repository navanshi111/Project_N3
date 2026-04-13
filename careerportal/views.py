from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Applicant, Employee

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user_type = form.cleaned_data.get("user_type")

            if user_type == "applicant":
                Applicant.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                    email=form.cleaned_data.get("email"),
                    bio=form.cleaned_data["bio"],
                    summary=form.cleaned_data["summary"],)

            elif user_type == "employee":
                Employee.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                    email=form.cleaned_data.get("email"),
                    company=form.cleaned_data["company"],)

            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'careerportal/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'careerportal/profile.html')

def home(request):
    return render(request, 'careerportal/home.html')

# Source: https://docs.djangoproject.com/en/5.2/intro/tutorial03/
# Source: Lecture 5 (Properties)