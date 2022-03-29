import re

from django import forms
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django_countries.widgets import CountrySelectWidget

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
from ..models import Teacher, School, Student
from ..permissions import teacher_login


class TeacherRegisterForm(forms.Form):
    """
    Register form for teacher.
    """

    error_messages = {
        "password_does_not_match": "您輸入的密碼不一致。",
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

    # captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

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

        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            # Any ValidationError raised by `clean` method will
            # not be associated with a particular field; it will have a special-case
            # association with the field named '__all__'.
            e = forms.ValidationError(self.error_messages["password_does_not_match"])
            self.add_error("password", e)
            self.add_error("confirm_password", e)

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
            self.user_cache = authenticate(username=user.username, password=password)

            # User credentials are invalid
            if self.user_cache is None:
                raise self.get_invalid_login_error()

            # User's email is not verified
            if not is_email_verified(self.user_cache):
                send_verification_email(self.request, self.user_cache)
                raise self.get_invalid_login_error()

            # User is inactive
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages["inactive"], code="inactive")

    def clean(self):
        email = self.cleaned_data.get("username", None)
        password = self.cleaned_data.get("password", None)

        if email is not None and password is not None:
            self.check_errors(email, password)

        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not teacher_login(user):
            raise self.get_invalid_login_error()


class TeacherEditForm(forms.Form):
    """
    Teacher edit account form.
    """

    error_messages = {
        "password_does_not_match": "您輸入的密碼不一致。",
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TeacherEditForm, self).__init__(*args, **kwargs)

    first_name = NameRegexField(
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "您的新名字", "class": "fName"}),
        help_text="您新的名字",
    )
    last_name = NameRegexField(
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "您的新姓氏", "class": "lName"}),
        help_text="您的新姓氏",
    )
    email = EmailField(
        required=False,
        help_text="新的電子郵件地址(選填)",
        widget=forms.EmailInput(attrs={"placeholder": "新的電子郵件地址(選填)"}),
    )
    password = CharField(
        required=False,
        help_text="新密碼(選填)",
        widget=forms.PasswordInput(attrs={"placeholder": "新密碼(選填)"}),
    )
    confirm_password = CharField(
        required=False,
        help_text="再次輸入新密碼(選填)",
        widget=forms.PasswordInput(attrs={"placeholder": "再次輸入新密碼(選填)"}),
    )
    current_password = CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "您目前的密碼"}),
        help_text="請輸入您目前的密碼",
    )

    def check_password_errors(self, password, confirm_password, current_password):
        if password != confirm_password:
            e = forms.ValidationError(self.error_messages["password_does_not_match"])
            self.add_error("password", e)
            self.add_error("confirm_password", e)

        if not self.user.check_password(current_password):
            raise forms.ValidationError("您目前的密碼輸入錯誤")

    def clean_password(self):
        return clean_password_helper(self, "password", PasswordStrength.TEACHER)

    def clean(self):
        if any(self.errors):
            return

        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        current_password = self.cleaned_data["current_password"]

        self.check_password_errors(password, confirm_password, current_password)

        return self.cleaned_data


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name", "postcode", "country"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "請輸入自定義學校名稱",
                },
            ),
            "postcode": forms.TextInput(
                attrs={"autocomplete": "off", "placeholder": "郵遞區號，如: 22053"}
            ),
            "country": CountrySelectWidget(layout="{widget}"),
        }
        help_texts = {
            "name": "自定義學校名稱",
            "postcode": "郵遞區號",
            "country": "國家或地區",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.current_school = kwargs.pop("current_school", None)
        super(OrganisationForm, self).__init__(*args, **kwargs)
        self.fields["postcode"].strip = False

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        validator = EmailValidator()

        if name:
            try:
                validator(name)
                is_email = True
            except forms.ValidationError:
                is_email = False

            if is_email:
                raise forms.ValidationError("請確認您輸入的名稱是否有效。")

        return name

    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode", None)

        if postcode:
            if len(postcode.replace(" ", "")) > 10 or len(postcode.replace(" ", "")) == 0:
                raise forms.ValidationError("請輸入有效的郵遞區號。")

        return postcode

    def clean(self):
        name = self.cleaned_data.get("name", None)
        postcode = self.cleaned_data.get("postcode", None)

        if name and postcode:
            try:
                school = School.objects.get(name=name, postcode=postcode)
            except School.DoesNotExist:
                return self.cleaned_data
            else:
                if not self.current_school or self.current_school.id != school.id:
                    raise forms.ValidationError("已經存在一個被註冊的學校名稱與郵遞區號。")

        return self.cleaned_data


class OrganisationJoinForm(forms.Form):
    fuzzy_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "請輸入學校名稱或郵遞區號"}
        ),
        help_text="請輸入學校名稱或郵遞區號",
    )

    chosen_org = forms.CharField(widget=forms.Select(), help_text="請選擇學校")

    def clean_chosen_org(self):
        chosen_org = self.cleaned_data.get("chosen_org", None)

        if chosen_org and not School.objects.filter(id=int(chosen_org)).exists():
            raise forms.ValidationError("無法識別學校名稱。")

        return chosen_org


class StudentCreationForm(forms.Form):
    names = CharField(
        label="姓名",
        widget=forms.Textarea(
            attrs={
                "placeholder": "您可以從 .csv 檔案匯入姓名或者是直接從檔案裡複制貼上到這個文字框",
                "class": "m-0",
            }
        ),
    )

    def __init__(self, klass, *args, **kwargs):
        self.klass = klass
        self.stripped_names = None
        super(StudentCreationForm, self).__init__(*args, **kwargs)

    @staticmethod
    def find_clashes(names, students, validation_errors):
        clashes_found = []

        for name in names:
            if students.filter(user__first_name__iexact=name).exists() and name not in clashes_found:
                validation_errors.append(forms.ValidationError(f"在班級裡已經存在名為 '{name}' 的學生"))
                clashes_found.append(name)

    @staticmethod
    def find_duplicates(names, lower_names, validation_errors):
        duplicates_found = []

        for duplicate in [name for name in names if lower_names.count(name.lower()) > 1]:
            if duplicate not in duplicates_found:
                validation_errors.append(forms.ValidationError(f"學生名 '{duplicate}' 最多只能新增一次"))
                duplicates_found.append(duplicate)

    @staticmethod
    def find_illegal_characters(names, validation_errors):
        for name in names:
            if re.match(re.compile(r"^[\w\s-]+$"), name) is None:
                validation_errors.append(
                    forms.ValidationError(f"姓名只能包涵英文、數字、空白字元、符號 '-' 與 '_'，您必須重新命名 '{name}'")
                )

    def validate_student_names(self, names):
        validation_errors = []

        if self.klass:
            students = Student.objects.filter(class_field=self.klass)

            self.find_clashes(names, students, validation_errors)

        lower_names = [name.lower() for name in names]

        self.find_duplicates(names, lower_names, validation_errors)
        self.find_illegal_characters(names, validation_errors)

        return validation_errors

    def clean(self):
        names = re.split(";|,|\n", self.cleaned_data.get("names", ""))
        names = list(map(lambda x: re.sub("[ \t]+", " ", x.strip()), names))
        names = [name for name in names if name != ""]

        validation_errors = self.validate_student_names(names)

        if len(validation_errors) > 0:
            raise forms.ValidationError(validation_errors)

        self.stripped_names = names

        return self.cleaned_data
