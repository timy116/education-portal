from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from .mixins import LoginRequiredNotRaiseErrorMixin
from ..forms.klass import ClassCreationForm
from ..forms.teacher import OrganisationJoinForm, OrganisationForm
from ..models import School, Student, Class
from ..permissions import independent_student_login, teacher_login


class IndependentStudentDashboard(LoginRequiredNotRaiseErrorMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/independent_student.html"
    login_url = reverse_lazy("independent_student_login")

    def test_func(self):
        return independent_student_login(self.request.user)


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

                return HttpResponseRedirect(reverse_lazy("onboarding_class"))

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_school.html",
        context={
            "create_form": create_form,
            "join_form": join_form,
            "teacher": teacher,
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
        form = ClassCreationForm()
    else:
        form = ClassCreationForm()

    classes = Class.objects.filter(teacher=teacher)

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_classes.html",
        context={"form": form, "classes": classes, "requests": requests}
    )
