from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
    
    # - Meta defines how the form maps to the database model.
    # - Email is included to support user identification and communication.