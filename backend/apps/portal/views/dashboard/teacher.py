import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from ...forms.klass import ClassCreationForm
from ...forms.teacher import (
    OrganisationJoinForm,
    OrganisationForm,
    StudentCreationForm,
)
from ...helpers.generators import (
    generate_access_code,
    generate_password,
    generate_login_id,
    generate_student_url,
)
from ...helpers.password import STUDENT_PASSWORD_LENGTH
from ...models import School, Student, Class
from ...permissions import teacher_login


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(teacher_login, login_url=reverse_lazy("teacher_login"))
def create_organisation(request):
    teacher = request.user.teacher
    create_form = OrganisationForm(user=request.user)
    join_form = OrganisationJoinForm()

    if request.method == "POST":
        if "create_organisation" in request.POST:
            create_form = OrganisationForm(request.POST, user=request.user)

            if create_form.is_valid():
                data = create_form.cleaned_data
                name = data.get("name", "")
                postcode = data.get("postcode", "").upper()
                country = data.get("country", "")
                town, lat, lng = ("", "0", "0")
                school = School.objects.create(
                    name=name,
                    postcode=postcode,
                    town=town,
                    latitude=lat,
                    longitude=lng,
                    country=country,
                )
                teacher.school = school
                teacher.is_admin = True
                teacher.save()
                messages.success(request=request, message=f"您的學校 '{teacher.school.name}' 已成功建立。")

                return HttpResponseRedirect(reverse_lazy("onboarding_classes"))

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_school.html",
        context={
            "create_form": create_form,
            "join_form": join_form,
            "teacher": teacher,
        },
    )


def process_edit_class(request, access_code: str, is_onboarding_done: bool, next_url: str):
    klass = get_object_or_404(Class, access_code=access_code)
    teacher = request.user.teacher
    students = Student.objects.filter(class_field=klass, user__is_active=True).order_by("user__first_name")

    if request.user.teacher != klass.teacher:
        raise Http404

    if request.method == "POST":
        new_students_form = StudentCreationForm(klass, data=request.POST)

        if new_students_form.is_valid():
            students_info = []

            for name in new_students_form.stripped_names:
                password = generate_password(STUDENT_PASSWORD_LENGTH)
                login_id, hashed_login_id = generate_login_id()
                student = Student.objects.school_factory(
                    klass=klass,
                    name=name,
                    password=password,
                    login_id=hashed_login_id,
                )
                login_url = generate_student_url(request, student, login_id)

                students_info.append(
                    {
                        "id": student.user.id,
                        "name": name,
                        "password": password,
                        "login_url": login_url,
                    }
                )

            return render(
                request=request,
                template_name="dashboard/teacher_onboarding_print.html",
                context={
                    "class": klass,
                    "students_info": students_info,
                    "is_onboarding_done": is_onboarding_done,
                    "query_data": json.dumps(students_info),
                    "class_url": request.build_absolute_uri(
                        reverse("student_login", kwargs={"access_code": klass.access_code})
                    )
                },
            )
    else:
        new_students_form = StudentCreationForm(klass)

    classes = Class.objects.filter(teacher=teacher)

    return render(
        request=request,
        template_name=next_url,
        context={
            "class": klass,
            "classes": classes,
            "students": students,
            "new_students_form": new_students_form,
            "num_students": len(students),
        },
    )


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(teacher_login, login_url=reverse_lazy("teacher_login"))
def create_class(request):
    teacher = request.user.teacher
    requests = Student.objects.filter(pending_class_request__teacher=teacher, user__is_active=True)

    if not teacher.school:
        return HttpResponseRedirect(reverse_lazy("onboarding_organisation"))

    if request.method == "POST":
        form = ClassCreationForm(request.POST)

        if form.is_valid():
            classmate_progress = bool(form.cleaned_data["classmate_progress"])
            klass = Class.objects.create(
                name=form.cleaned_data["class_name"],
                teacher=teacher,
                access_code=generate_access_code(),
                can_view_classmates_data=classmate_progress,
            )

            messages.success(request, f"您的班級 '{klass.name}' 已建立成功。")

            return HttpResponseRedirect(reverse_lazy("onboarding_class", kwargs={"access_code": klass.access_code}))
    else:
        form = ClassCreationForm()

    classes = Class.objects.filter(teacher=teacher)

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_classes.html",
        context={"form": form, "classes": classes, "requests": requests}
    )


def edit_class(request, access_code):
    return process_edit_class(
        request,
        access_code,
        is_onboarding_done=False,
        next_url="dashboard/teacher_onboarding_students.html",
    )
