from django.conf.urls import url

from ..views.login import (
    IndependentStudentLoginView, TeacherLoginView
)

urlpatterns = [
    url(r"^independent/$", IndependentStudentLoginView.as_view(), name="independent_student_login"),
    url(r"^teacher/$", TeacherLoginView.as_view(), name="teacher_login"),
]
