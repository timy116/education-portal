from django.conf.urls import url

from ..views.email import (
    VerifyEmailView,
    verify_email
)

urlpatterns = [
    url(r"^verify/$", VerifyEmailView.as_view(), name="email_verification"),
    url(r"^verify/(?P<token>[0-9a-f]+)/$", verify_email, name="verify_email"),
]
