from django import forms

ERROR_MESSAGES = {
    'required': '此欄位必填。',
    "min_length": '此欄位長度最少需 %(limit_value)d 個字元。',
    "max_length": '此欄位長度最多 %(limit_value)d 個字元。',
    'invalid': '檢測到無效字元。',
}


class CharField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(error_messages=ERROR_MESSAGES, **kwargs)


class NameRegexField(forms.RegexField):
    PATTERN = r"^([^\d^\W]\s?|[\-])+$"

    def __init__(self, **kwargs):
        super().__init__(self.PATTERN, error_messages=ERROR_MESSAGES, **kwargs)


class UsernameRegexField(NameRegexField):
    PATTERN = r"^([^\W]-?)+$"


class EmailField(forms.EmailField):

    def __init__(self, **kwargs):
        ERROR_MESSAGES["invalid"] = "無效的電子郵件地址。"

        super().__init__(error_messages=ERROR_MESSAGES, **kwargs)
