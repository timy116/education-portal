from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms

from apps.portal.helpers.password import (
    PasswordStrength,
    clean_password_helper
)


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
