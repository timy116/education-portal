from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from apps.portal.email import (
    is_email_verified,
    send_verification_email
)
from apps.portal.helpers.password import (
    PasswordStrength,
    clean_password_helper
)
from apps.portal.models import Teacher


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

    first_name = forms.CharField(
        max_length=100,
        help_text="請輸入您的名字",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "小明"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        help_text="請輸入您的姓氏",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "王"}
        ),
    )
    email = forms.EmailField(
        help_text="請輸入您的電子郵件地址",
        widget=forms.EmailInput(
            attrs={"autocomplete": "off",
                   "placeholder": "user@example.com"}
        ),
    )
    password = forms.CharField(
        help_text="請輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "長度至少 10 個字元"}
        ),
    )
    confirm_password = forms.CharField(
        help_text="請再次輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "再次輸入您的密碼"}
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def clean_password(self):
        return clean_password_helper(self, "password", PasswordStrength.TEACHER)

    def clean(self):
        if any(self.errors):
            return

        password = self.cleaned_data.get("password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)

        check_passwords(password, confirm_password)

        return self.cleaned_data


class TeacherLoginForm(AuthenticationForm):
    ERROR_MESSAGE = "錯誤！請確認您資料是否輸入正確，並且已通過電子郵件驗證。"

    username = forms.EmailField(
        label="電子郵件地址", widget=forms.EmailInput(attrs={"autocomplete": "off", "placeholder": "user@address.com"})
    )
    password = forms.CharField(
        label="密碼", widget=forms.PasswordInput(attrs={"autocomplete": "off", "placeholder": "您的密碼"})
    )

    def raise_error(self):
        """
        Raise a login failed exception.
        :return: None
        """

        raise forms.ValidationError(self.ERROR_MESSAGE)

    def check_errors(self, email, password):
        try:
            # Teacher does not exist
            teacher = Teacher.objects.get(user__email=email)
        except Teacher.DoesNotExist:
            self.raise_error()
        else:
            user = teacher.user
            user = authenticate(username=user.username, password=password)

            # User credentials are invalid
            if user is None:
                self.raise_error()

            # The user's email is not verified
            if not is_email_verified(user):
                send_verification_email(self.request, user)
                self.raise_error()

    def clean(self):
        email = self.cleaned_data.get("username", None)
        password = self.cleaned_data.get("password", None)

        if email is not None and password is not None:
            self.check_errors(email, password)

        return self.cleaned_data
