from .mixins import LoginRequiredNotRaiseErrorMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from ..permissions import independent_student_login


class IndependentStudentDashboard(LoginRequiredNotRaiseErrorMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/independent_student.html"
    login_url = reverse_lazy("independent_student_login")

    def test_func(self):
        return independent_student_login(self.request.user)


def organisation_create(request):
    pass
