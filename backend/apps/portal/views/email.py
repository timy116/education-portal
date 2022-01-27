from django.views.generic.base import TemplateView


class VerifyEmailView(TemplateView):
    template_name = "email/email_verification.html"


def verify_email(request, token):
    pass
