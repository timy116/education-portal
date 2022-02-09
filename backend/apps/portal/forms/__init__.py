from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class BaseLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("錯誤！請確認您資料是否輸入正確。"),
        "inactive": _("此帳號未啟用，請先驗證您的電子郵件信箱。"),
    }

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login"
        )

    def get_inactive_login_error(self):
        return forms.ValidationError(
            self.error_messages["inactive"],
            code="invalid_login"
        )
