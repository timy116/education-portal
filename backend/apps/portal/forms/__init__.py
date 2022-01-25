from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class BaseLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("錯誤！請確認您資料是否輸入正確，並且已通過電子郵件驗證。"),
        "inactive": _("此帳號未啟用。"),
    }

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login"
        )
