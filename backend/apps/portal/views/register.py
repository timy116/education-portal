from django.shortcuts import render

from ..email import send_verification_email
from ..forms.student import IndependentStudentRegisterForm
from ..forms.teacher import TeacherRegisterForm
from ..models import Student


def register(request):
    """
    註冊分為老師(Teacher) 和 獨立學生(Independent)
    """

    teacher_prefix = "teacher_reg"
    ind_prefix = "ind_reg"

    if request.user.is_authenticated:
        ...

    teacher_form = TeacherRegisterForm(prefix=teacher_prefix)
    ind_form = IndependentStudentRegisterForm(prefix=ind_prefix)

    if request.method == "POST":
        # If teacher sign up
        if f"{teacher_prefix}-email" in request.POST:
            teacher_form = TeacherRegisterForm(data=request.POST, prefix=teacher_prefix)

            if teacher_form.is_valid():
                data = teacher_form.cleaned_data

                # Dispatch to teacher handler
                return teacher_register_form_handler(request, data)

        # If independent sign up
        else:
            ind_form = IndependentStudentRegisterForm(data=request.POST, prefix=ind_prefix)

            if ind_form.is_valid():
                data = ind_form.cleaned_data

                # Dispatch to independent handler
                return independent_student_register_form_handler(request, data)

    # GET request
    return render(
        request=request,
        template_name="register.html",
        context={
            "teacher_form": teacher_form,
            "ind_form": ind_form,
        }
    )


def teacher_register_form_handler(request, data):
    ...


def independent_student_register_form_handler(request, data):
    student = Student.objects.independent_student_factory(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        name=data["name"]
    )
    send_verification_email(request, student.user)

    return render(request, "email/email_verification.html", context={"is_teacher": False})
