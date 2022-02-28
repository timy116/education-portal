from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.urls.exceptions import NoReverseMatch

from ..forms.student import IndependentStudentLoginForm
from ..forms.teacher import TeacherLoginForm
from ..models import UserSession

User = get_user_model()


class IndependentStudentLoginView(LoginView):
    template_name = "login/independent_student.html"
    form_class = IndependentStudentLoginForm
    success_url = reverse_lazy("independent_student_dashboard")

    def get_success_url(self):
        try:
            return super().get_success_url()
        except NoReverseMatch:
            return self.success_url

    def form_valid(self, form):
        messages.info(
            self.request,
            f"<strong>您目前以獨立學生的身份登入，如果您想加入一個學校，請至"
            f"<a href='#' id='student_join_school_link'>申請加入學校</a>"
            f"</strong>",
            extra_tags="safe",
        )

        username = self.request.POST.get("username")
        user = User.objects.get(username=username)
        session = UserSession(user=user)
        session.save()

        return super().form_valid(form)


class TeacherLoginView(LoginView):
    template_name = "login/teacher.html"
    form_class = TeacherLoginForm

    def redirect_to(self, teacher):
        if teacher.has_school:
            pass
        else:
            return reverse_lazy("onboarding_organisation")

    def get_success_url(self):
        try:
            return super().get_success_url()
        except NoReverseMatch:
            return self.redirect_to(self.request.user.userprofile.teacher)
