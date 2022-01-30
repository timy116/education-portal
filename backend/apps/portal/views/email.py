from django.contrib import messages as messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView

from apps.portal.models import EmailVerification
from apps.portal.permissions import teacher_login, independent_student_login


class VerifyEmailView(TemplateView):
    template_name = "email/email_verification.html"


def verify_email(request, token):
    verifications = EmailVerification.objects.filter(token=token)

    if EmailVerification.objects.is_verification_failed(verifications):
        return render(request, "email/email_verification_failed.html")

    verification = verifications[0]
    verification.verified = True
    verification.save()

    user = verification.user

    if verification.email:
        user.email = verification.email

        if teacher_login(user):
            user.username = verification.email

        user.save()
        user.email_verifications.exclude(email=user.email).delete()
        messages.success(request, message="您的電子郵件地址已驗證完成，請登入。")

        if independent_student_login(user):
            login_url = reverse("independent_student_login")
        else:
            login_url = reverse("teacher_login")

        return HttpResponseRedirect(redirect_to=login_url)
