from django.conf.urls import url

from ..views.register import register

urlpatterns = [
    url(r"^$", register, name="register"),
]
