from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.contrib.auth import authenticate

from apps.portal.email import (
    is_email_verified,
    send_verification_email
)
from apps.portal.helpers.password import (
    PasswordStrength,
    clean_password_helper
)
from . import BaseLoginForm
from ..fields import (
    CharField, NameRegexField, EmailField
)
from ..models import Teacher


def check_passwords(password, confirm_password):
    """
    檢查兩次密碼是否輸入一致
    """

    if password is not None and password != confirm_password:
        raise forms.ValidationError("您輸入的密碼不一致。")


class TeacherRegisterForm(forms.Form):
    """
    Register form for teacher.
    """
    error_messages = {
        'required': '此欄位必填。',
    }

    first_name = NameRegexField(
        max_length=15,
        help_text="請輸入您的名字",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "小明", "class": ""}
        ),
    )
    last_name = NameRegexField(
        max_length=10,
        help_text="請輸入您的姓氏",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "王", "class": ""}
        ),
    )
    email = EmailField(
        help_text="請輸入您的電子郵件地址",
        widget=forms.EmailInput(
            attrs={"autocomplete": "off",
                   "placeholder": "user@example.com", "class": ""}
        ),
    )
    password = CharField(
        help_text="請輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "長度至少 10 個字元", "class": ""}
        ),
    )
    confirm_password = CharField(
        help_text="請再次輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "再次輸入您的密碼", "class": ""}
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Teacher.objects.is_email_already_used(email):
            raise forms.ValidationError("此電子郵件地址已被使用。")

        return email

    def clean_password(self):
        return clean_password_helper(self, "password", PasswordStrength.TEACHER)

    def clean(self):
        if any(self.errors):
            return

        password = self.cleaned_data.get("password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)

        check_passwords(password, confirm_password)

        return self.cleaned_data


class TeacherLoginForm(BaseLoginForm):
    username = forms.EmailField(
        label="電子郵件地址", widget=forms.EmailInput(attrs={"autocomplete": "off", "placeholder": "user@address.com"})
    )
    password = forms.CharField(
        label="密碼", widget=forms.PasswordInput(attrs={"autocomplete": "off", "placeholder": "您的密碼"})
    )

    def check_errors(self, email, password):
        try:
            # Teacher does not exist
            teacher = Teacher.objects.get(user__email=email)
        except Teacher.DoesNotExist:
            raise self.get_invalid_login_error()
        else:
            user = teacher.user
            user = authenticate(username=user.username, password=password)

            # User credentials are invalid
            if user is None:
                raise self.get_invalid_login_error()

            # User's email is not verified
            if not is_email_verified(user):
                send_verification_email(self.request, user)
                raise self.get_invalid_login_error()

            # User is inactive
            if not user.is_active:
                raise forms.ValidationError(self.error_messages["inactive"], code="inactive")

    def clean(self):
        email = self.cleaned_data.get("username", None)
        password = self.cleaned_data.get("password", None)

        if email is not None and password is not None:
            self.check_errors(email, password)

        return self.cleaned_data
