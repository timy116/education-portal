from .mixins import LoginRequiredNotRaiseErrorMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.urls import reverse_lazy
from ..permissions import independent_student_login
from ..forms.teacher import OrganisationJoinForm, OrganisationForm


class IndependentStudentDashboard(LoginRequiredNotRaiseErrorMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/independent_student.html"
    login_url = reverse_lazy("independent_student_login")

    def test_func(self):
        return independent_student_login(self.request.user)


def organisation_create(request):
    teacher = request.user.teacher
    create_form = OrganisationForm(user=request.user)
    join_form = OrganisationJoinForm()

    return render(
        request=request,
        template_name="dashboard/teacher_onboarding_school.html",
        context={
            "create_form": create_form,
            "join_form": join_form,
            "teacher": teacher,
        },
    )
