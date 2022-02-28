from django.conf.urls import url
from ..views.dashboard import (
    IndependentStudentDashboard, organisation_create
)

urlpatterns = [
    url(r"^independent/$", IndependentStudentDashboard.as_view(), name="independent_student_dashboard"),
    url(r"^onboarding-organisation/$", organisation_create, name="onboarding_organisation"),
]
