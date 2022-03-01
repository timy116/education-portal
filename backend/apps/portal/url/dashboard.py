from django.conf.urls import url
from ..views.dashboard import (
    IndependentStudentDashboard, create_organisation, create_class
)

urlpatterns = [
    url(r"^independent/$", IndependentStudentDashboard.as_view(), name="independent_student_dashboard"),
    url(r"^onboarding-organisation/$", create_organisation, name="onboarding_organisation"),
    url(r"^onboarding-class/$", create_class, name="onboarding_class"),
]
