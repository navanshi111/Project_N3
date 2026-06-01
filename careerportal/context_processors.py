from .models import Applicant, Employee

def user_roles(request):
    is_applicant = False
    is_employee = False

    if request.user.is_authenticated:
        is_applicant = Applicant.objects.filter(
            id=request.user.id
        ).exists()

        is_employee = Employee.objects.filter(
            id=request.user.id
        ).exists()

    return {
        'is_applicant': is_applicant,
        'is_employee': is_employee,
    }