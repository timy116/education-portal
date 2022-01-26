import datetime
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.portal.models import EmailVerification

User = get_user_model()


def generate_token(user: User, email="", pre_verified=False) -> EmailVerification:
    return EmailVerification.objects.create(
        user=user,
        email=email,
        token=uuid4().hex[:30],
        expiry=timezone.now() + datetime.timedelta(hours=1),
        verified=pre_verified,
    )


def is_email_verified(user: User) -> bool:
    try:
        verification = EmailVerification.objects.filter(user=user).latest("user")
    except EmailVerification.DoesNotExist:
        return False
    else:
        return verification.verified
