from django import template
from django.contrib.auth import get_user_model
from ..models import EmailVerification

User = get_user_model()
register = template.Library()


@register.filter
def is_logged_in(user):
    return user and user.is_authenticated


@register.filter
def is_verified(user) -> bool:
    try:
        verification = EmailVerification.objects.filter(user=user).latest("user")
    except EmailVerification.DoesNotExist:
        return False
    else:
        return verification.verified


@register.filter
def is_independent_student(user):
    return (
        is_logged_in(user)
        and user.userprofile
        and hasattr(user.userprofile, "student")
        and user.userprofile.student.is_independent()
    )


@register.filter
def is_logged_in_as_teacher(user):
    return is_logged_in(user) and user.userprofile and hasattr(user.userprofile, "teacher")


@register.filter
def get_username(user):
    username = ""

    if hasattr(user, "userprofile"):
        if hasattr(user.userprofile, "student"):
            username = user.first_name
        elif hasattr(user.userprofile, "teacher"):
            username = user.first_name + " " + user.last_name

    return username
