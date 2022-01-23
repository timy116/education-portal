from apps.portal.forms.student import IndependentStudentRegisterForm
from apps.portal.forms.teacher import TeacherRegisterForm
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def register(request):
    """
    註冊分為老師(Teacher) 和 獨立學習者(Independent)
    """

    teacher_prefix = "teacher_reg"
    ind_prefix = "ind_reg"
    email_f_name = "teacher_email"

    if request.user.is_authenticated:
        ...

    teacher_form = TeacherRegisterForm(prefix=teacher_prefix)
    ind_form = IndependentStudentRegisterForm(prefix=ind_prefix)

    if request.method == "POST":
        # If teacher sign up
        if f"{teacher_prefix}-{email_f_name}" in request.POST:
            teacher_form = TeacherRegisterForm(
                data=request.POST,
                prefix=teacher_prefix
            )

            if teacher_form.is_valid():
                data = teacher_form.cleaned_data

                # Dispatch to teacher handler
                return teacher_register_form_handler(request, data)

        # If independent sign up
        else:
            ind_form = IndependentStudentRegisterForm(
                data=request.POST,
                prefix=ind_prefix
            )

            if ind_form.is_valid():
                data = ind_form.cleaned_data

                # Dispatch to Independent handler
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
    ...
