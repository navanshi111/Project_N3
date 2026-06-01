from django.core.exceptions import ValidationError

def validate_pdf(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")