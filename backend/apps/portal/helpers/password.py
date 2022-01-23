import re
from enum import Enum, auto

from django import forms

MOST_USED_PASSWORDS = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "password",
    "123456",
]


class PasswordStrength(Enum):
    STUDENT = auto()
    INDEPENDENT = auto()
    TEACHER = auto()

    def is_password_strength_enough(
        self, password, minimum_password_length, upper=True, lower=True, numbers=True, special_char=True
    ) -> bool:
        """
        檢查密碼是否符合複雜度原則(英文大小寫字母、數字及特殊符號字元)
        """

        return (
            len(password) >= minimum_password_length
            and (not upper or re.search(r"[A-Z]", password))
            and (not lower or re.search(r"[a-z]", password))
            and (not numbers or re.search(r"[0-9]", password))
            and (not special_char or re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password))
            and (password not in MOST_USED_PASSWORDS)
        )

    def password_tester(self, password):
        special_char = False
        minimum_password_length = 6
        error_message = "您的密碼不符合複雜度原則(長度至少 %s 個字元且包含英文大小寫字母、數字及特殊符號字元)。"

        # 老師密碼長度需要 10，且必須包含特殊字元
        if self is PasswordStrength.TEACHER:
            minimum_password_length = 10
            special_char = True

        # 獨立學習者密碼長度需要 8
        elif self is PasswordStrength.INDEPENDENT:
            minimum_password_length = 8

        if password and self.is_password_strength_enough(
            password=password,
            minimum_password_length=minimum_password_length,
            upper=True,
            lower=True,
            numbers=True,
            special_char=special_char
        ):
            return password

        raise forms.ValidationError(error_message % minimum_password_length)


def clean_password_helper(self, attr, strength: PasswordStrength):
    pwd = self.cleaned_data.get(attr, None)
    cleaned_pwd = strength.password_tester(pwd)

    return cleaned_pwd
