from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company

class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employee', 'Employee'),)

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    # Applicant fields
    bio = forms.CharField(required=False)
    summary = forms.CharField(required=False)

    # Employee field
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    # - Meta defines how the form maps to the database model.
    # - Email is included to support user identification and communication.