from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from ..mixins import LoginRequiredNotRaiseErrorMixin
from ...forms.klass import ClassCreationForm
from ...helpers.generators import generate_access_code
from ...permissions import independent_student_login, teacher_login


class IndependentStudentDashboard(LoginRequiredNotRaiseErrorMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/independent_student.html"
    login_url = reverse_lazy("independent_student_login")

    def test_func(self):
        return independent_student_login(self.request.user)
