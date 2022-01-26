from django.conf.urls import url, include

urlpatterns = [
    url(r"^register/", include("apps.portal.url.register")),
    url(r"^login/", include("apps.portal.url.login")),
]
