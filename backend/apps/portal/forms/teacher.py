from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms


class TeacherRegisterForm(forms.Form):
    """
    Register form for teacher.
    """

    first_name = forms.CharField(
        max_length=100,
        help_text="請輸入您的名字",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "名字，例如: 小明"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        help_text="請輸入您的姓氏",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "placeholder": "姓氏，例如: 王"}
        ),
    )
    email = forms.EmailField(
        help_text="請輸入您的電子郵件地址",
        widget=forms.EmailField(
            attrs={"autocomplete": "off",
                   "placeholder": "電子郵件，例如: user@example.com"}
        ),
    )
    password = forms.CharField(
        help_text="請輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "長度至少為 10 個字元"}
        ),
    )
    confirm_password = forms.CharField(
        help_text="請再次輸入密碼",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "off", "placeholder": "密碼確認"}
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def clean_password(self):
        ...

        return self

    def clean(self):
        ...

        return self.cleaned_data
