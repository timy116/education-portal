from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login


class LoginRequiredNotRaiseErrorMixin(LoginRequiredMixin):
    """
    Overwrites Django's ``LoginRequiredMixin`` to not raise an error.
    """

    def handle_no_permission(self):
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )
