from apps.portal.models import EmailVerification
from django.contrib.auth import get_user_model


User = get_user_model()


def is_email_verified(user: User) -> bool:
    try:
        verification = EmailVerification.objects.filter(user=user).latest("user")
    except EmailVerification.DoesNotExist:
        return False
    else:
        return verification.verified
