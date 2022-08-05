import csv
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from ...forms.klass import ClassCreationForm
from ...forms.teacher import (
    OrganisationJoinForm,
    OrganisationForm,
    StudentCreationForm,
    TeacherEditForm,
)
from ...helpers.generators import (
    generate_access_code,
    generate_password,
    generate_login_id,
    generate_student_url,
)
from ...helpers.password import STUDENT_PASSWORD_LENGTH
from ...models import School, Student, Class, Teacher
from ...permissions import teacher_login


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(teacher_login, login_url=reverse_lazy("teacher_login"))
def dashboard(request):
    teacher = request.user.teacher

    if not teacher.school:
        return HttpResponseRedirect(reverse_lazy("onboarding_organisation"))

    school = teacher.school
    coworkers = Teacher.objects.filter(pending_join_request=school).order_by("user__last_name", "user__first_name")
    join_requests = Teacher.objects.filter(pending_join_request=school).order_by("user__last_name", "user__first_name")
    requests = Student.objects.filter(pending_class_reqest__teacher=teacher)
    update_school_form = OrganisationForm(user=request.user, current_school=school)

    update_school_form.fields["name"].initial = school.name
    update_school_form.fields["postcode"].initial = school.postcode
    update_school_form.fields["country"].initial = school.country

    create_class_form = ClassCreationForm()
    update_account_form = TeacherEditForm(request.user)

    update_account_form.fields["first_name"].initial = request.user.first_name
    update_account_form.fields["last_name"].initial = request.user.last_name

    anchor = ""
    show_onboarding_complete = False

    if request.method == "POST":
        pass

    classes = Class.objects.filter(teacher=teacher)

    return render(
        request,
        "dashboard/teacher_dashboard.html",
        {
            "teacher": teacher,
            "classes": classes,
            "is_admin": teacher.is_admin,
            "coworkers": coworkers,
            "join_requests": join_requests,
            "requests": requests,
            "update_school_form": update_school_form,
            "create_class_form": create_class_form,
            "update_account_form": update_account_form,
            "anchor": anchor,
            "show_onboarding_complete": show_onboarding_complete,
        },
    )


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


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(teacher_login, login_url=reverse_lazy("teacher_login"))
def edit_class(request, access_code):
    return process_edit_class(
        request,
        access_code,
        is_onboarding_done=True,
        next_url="dashboard/teacher_onboarding_students.html",
    )


@login_required(login_url=reverse_lazy("teacher_login"))
@user_passes_test(teacher_login, login_url=reverse_lazy("teacher_login"))
def download_csv(request, access_code):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="student_login_urls.csv"'

    klass = get_object_or_404(Class, access_code=access_code)

    if klass.teacher.user != request.user:
        return Http404

    data = []
    class_url = request.build_absolute_uri(reverse("student_login", kwargs={"access_code": access_code}))

    if request.method == "POST":
        data = json.loads(request.POST.get("data", "[]"))

    if data:
        writer = csv.writer(response)
        writer.writerow([access_code, class_url])

        for student in data:
            writer.writerow([student["name"], student["password"], student["login_url"]])

    return response


def test(request):
    teacher = request.user.teacher
    klass = teacher.class_teacher.all()[0]
    students_info = []

    students_info.append(
        {
            "id": 1,
            "name": 'Ben',
            "password": 'dzwwmb',
            "login_url": 'http://127.0.0.1:8000/login/u/12/3ed57463a3974d7eb3e4cbb94043e0cc/',
        }
    )

    students_info.append(
        {
            "id": 2,
            "name": 'Cindy',
            "password": 'txnelj',
            "login_url": 'http://127.0.0.1:8000/login/u/13/4b3be8049360492a833c59fa6d21edd1/',
        }
    )

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_print.html",
        context={
            "class": klass,
            "students_info": students_info,
            "is_onboarding_done": False,
            "query_data": json.dumps(students_info),
            "class_url": request.build_absolute_uri(
                reverse("student_login", kwargs={"access_code": klass.access_code})
            )
        },
    )
