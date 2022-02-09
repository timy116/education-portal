from django.conf.urls import url
from ..views.dashboard import IndependentStudentDashboard

urlpatterns = [
    url(r"^independent/$", IndependentStudentDashboard.as_view(), name="independent_student_dashboard"),
]
