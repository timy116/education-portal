from django.conf.urls import url
from ..views.login import IndependentStudentLoginView

urlpatterns = [
    url(r"^independent/$", IndependentStudentLoginView.as_view(), name="independent_student_login"),
]
