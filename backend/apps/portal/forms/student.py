import re

from backend.apps.portal.helpers.password import (PasswordStrength,
                                                  clean_password_helper)
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms


class IndependentStudentRegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        help_text="請輸入您的大名",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "全名，例如: 王小明"}
        ),
    )

    username = forms.CharField(
        max_length=100,
        help_text="請輸入使用者名稱(帳號)",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "使用者帳號，例如: xiaoMing123"}
        ),
    )
    email = forms.EmailField(
        help_text="請輸入您的電子郵件地址",
        widget=forms.EmailInput(
            attrs={"autocomplete": "off", "placeholder": "電子郵件，例如: user@example.com"}
        ),
    )
    password = forms.CharField(
        help_text="請輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "長度至少 8 個字元"}
        ),
    )

    confirm_password = forms.CharField(
        help_text="請再次輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "密碼確認"}
        ),
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def clean_name(self):
        name = self.cleaned_data.get("name", None)

        if re.match(re.compile("^[\w ]+$"), name) is None:
            raise forms.ValidationError("姓名只能包含文字、數字、符號('-', '_')與空白字元。")

        return name

    def clean_username(self):
        username = self.cleaned_data.get("username", None)

        if re.match(re.compile("[\w]+"), username) is None:
            raise forms.ValidationError(
                "使用者名稱(帳號)只能包含文字、數字、符號('-', '_')與空白字元。"
            )

        return username

    def clean_password(self):
        return clean_password_helper(self, "password", PasswordStrength.INDEPENDENT)

    def clean(self):
        password = self.cleaned_data.get("password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")

        return self.cleaned_data
