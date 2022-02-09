from django.conf.urls import url, include

urlpatterns = [
    url(r"^register/", include("apps.portal.url.register")),
    url(r"^login/", include("apps.portal.url.login")),
    url(r"^email/", include("apps.portal.url.email")),
    url(r"^dashboard/", include("apps.portal.url.dashboard")),

]
