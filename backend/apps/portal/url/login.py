from django.conf.urls import url

from ..helpers.re import ACCESS_CODE_REGEX
from ..views.login import (
    IndependentStudentLoginView,
    TeacherLoginView,
    StudentLoginView,
    student_direct_login,
)

urlpatterns = [
    url(r"^independent/$", IndependentStudentLoginView.as_view(), name="independent_student_login"),
    url(r"^teacher/$", TeacherLoginView.as_view(), name="teacher_login"),
    url(
        rf"^student/(?P<access_code>{ACCESS_CODE_REGEX})/(?:(?P<login_type>classform)/)?$",
        StudentLoginView.as_view(),
        name="student_login",
    ),
    url(r"^u/(?P<user_id>[0-9]+)/(?P<login_id>[a-z0-9]+)/$", student_direct_login, name="student_direct_login"),
]
