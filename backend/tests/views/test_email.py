import pytest
from tests import factories as f
from django.urls import reverse
from apps.portal.models import EmailVerification
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_email_verify_verification_failed(client):
    teacher = f.TeacherFactory.create()
    f.EmailVerificationFactory(user=teacher.user)

    resp = client.get_soup(reverse("verify_email", kwargs={"token": "12345abcde"}))

    assert "您的電子郵件地址驗證失敗" == resp.select("h4")[0].text


def test_email_verify_success(client):
    teacher = f.TeacherFactory.create()
    verification = f.EmailVerificationFactory(user=teacher.user)

    resp = client.get(reverse("verify_email", kwargs={"token": verification.token}))

    verification = EmailVerification.objects.get(pk=verification.pk)
    user = User.objects.get(pk=teacher.user.pk)

    assert "/login/teacher/" in resp["Location"]
    assert verification.verified is True
    assert user.username == verification.email
