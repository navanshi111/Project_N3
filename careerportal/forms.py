from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Job , Application 

class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employee', 'Employee'),)

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    email = forms.EmailField(required=True)

    bio = forms.CharField(required=False)
    summary = forms.CharField(required=False)

    OTHER_CHOICE = 'other'

    company = forms.ChoiceField(required=False)
    new_company = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        companies = Company.objects.all()
        choices = [(c.id, c.name) for c in companies]
        choices.append((self.OTHER_CHOICE, "Other"))

        self.fields['company'].choices = choices

    def clean(self):
        cleaned_data = super().clean()

        user_type = cleaned_data.get("user_type")
        bio = cleaned_data.get("bio")
        summary = cleaned_data.get("summary")
        company = cleaned_data.get("company")
        new_company = cleaned_data.get("new_company")

        # Applicant validation
        if user_type == "applicant":
            if not bio or not summary:
                raise forms.ValidationError("Applicants must fill bio and summary.")

        # Employee validation
        elif user_type == "employee":
            if not company:
                raise forms.ValidationError("Employees must select a company.")

            if company == "other":
                if not new_company:
                    raise forms.ValidationError("Please enter a company name.")

                # Preventing duplicate companies, is also case-insensitive
                existing = Company.objects.filter(name__iexact=new_company.strip()).first()
                if existing:
                    cleaned_data["company"] = existing.id

        return cleaned_data
    
    #  Meta defines how the form maps to the database model.
    #  Email is included to support user identification.



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_degree', 'deadline', 'job_type', 'pay_status', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'required_degree': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'pay_status': forms.Select(attrs={'class': 'form-control'}),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. contact@company.com | +47 123 45 678 | www.company.com'
            }),
        }
        labels = {
            'contact_info': 'Contact Information',
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['text', 'cv']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your cover letter here...'
            }),
        }
        labels = {
            'text': 'Cover Letter',
            'cv': 'Attach CV (optional)',
        }