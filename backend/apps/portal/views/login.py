from django.contrib.auth.views import LoginView

from ..forms.student import IndependentStudentLoginForm


class IndependentStudentLoginView(LoginView):
    template_name = "login/independent_student.html"
    form_class = IndependentStudentLoginForm
