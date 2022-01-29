import pytest
from django.urls import reverse

from apps.portal.email import (
    send_verification_email,
    SUBJECT_TEMPLATE,
    SUBJECT_PREFIX,
    EMAIL_VERIFICATION_SUBJECT,
)
from tests import factories as f

pytestmark = pytest.mark.django_db


def test_verification_email(client, outbox):
    user = f.UserFactory.create()
    request = client.factory.request()

    send_verification_email(request, user)

    subject = SUBJECT_TEMPLATE % {"prefix": SUBJECT_PREFIX, "subject": EMAIL_VERIFICATION_SUBJECT}
    verification = user.email_verifications.first()
    verification_url = request.build_absolute_uri(reverse("verify_email", kwargs={"token": verification.token}))

    assert len(outbox) == 1
    assert outbox[0].subject == subject
    assert verification_url in outbox[0].body
