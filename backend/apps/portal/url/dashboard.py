from django.conf.urls import url
from ..views.dashboard.student import IndependentStudentDashboard
from ..views.dashboard.teacher import (
    dashboard, create_organisation, create_class, edit_class, download_csv, test
)
from ..helpers.re import ACCESS_CODE_REGEX

urlpatterns = [
    url(r"^independent/$", IndependentStudentDashboard.as_view(), name="independent_student_dashboard"),
    url(r"^onboarding-organisation/$", create_organisation, name="onboarding_organisation"),
    url(r"^onboarding-classes/$", create_class, name="onboarding_classes"),
    url(rf"^onboarding-class/(?P<access_code>{ACCESS_CODE_REGEX})$", edit_class, name="onboarding_class"),
    url(
        rf"^onboarding-class/(?P<access_code>{ACCESS_CODE_REGEX})/download-csv/$",
        download_csv,
        name="teacher_download_csv"
    ),
    url(r"^teacher-dashboard/$", dashboard, name="teacher_dashboard"),
    url(r"^teacher-test/$", test, name="teacher_test"),
]
