from django.contrib.auth.views import LoginView

from ..forms.student import IndependentStudentLoginForm
from ..forms.teacher import TeacherLoginForm


class IndependentStudentLoginView(LoginView):
    template_name = "login/independent_student.html"
    form_class = IndependentStudentLoginForm


class TeacherLoginView(LoginView):
    template_name = "login/teacher.html"
    form_class = TeacherLoginForm
