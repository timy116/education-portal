from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms

from apps.portal.email.helper import is_email_verified
from apps.portal.helpers.password import (
    PasswordStrength, clean_password_helper
)
from . import BaseLoginForm
from ..fields import (CharField, NameRegexField, UsernameRegexField, EmailField)
from ..models import Student


class IndependentStudentRegisterForm(forms.Form):
    name = NameRegexField(
        max_length=100,
        help_text="請輸入您的大名",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "王小明", "class": "" }
        ),
    )

    username = UsernameRegexField(
        max_length=100,
        help_text="請輸入使用者名稱(帳號)",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "xiaoMing123", "class": ""}
        ),
    )
    email = EmailField(
        help_text="請輸入您的電子郵件地址",
        widget=forms.EmailInput(
            attrs={"autocomplete": "off", "placeholder": "user@example.com", "class": ""}
        ),
    )
    password = CharField(
        help_text="請輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "長度至少 8 個字元", "class": ""}
        ),
    )

    confirm_password = CharField(
        help_text="請再次輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "再次輸入您的密碼", "class": ""}
        ),
    )

    # captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def clean_username(self):
        username = self.cleaned_data["username"]

        if Student.objects.is_username_already_used(username):
            raise forms.ValidationError("此使用者名稱已被使用。")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Student.objects.is_email_already_used(email):
            raise forms.ValidationError("此電子郵件地址已被使用。")

        return email

    def clean_password(self):
        return clean_password_helper(self, "password", PasswordStrength.INDEPENDENT)

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")

        return self.cleaned_data


class IndependentStudentLoginForm(BaseLoginForm):
    username = forms.CharField(label="使用者名稱", widget=forms.TextInput())
    password = forms.CharField(label="密碼", widget=forms.PasswordInput())

    def confirm_login_allowed(self, user):
        if not is_email_verified(user):
            raise self.get_invalid_login_error()
