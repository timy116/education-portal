from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    url(r"^", include("apps.portal.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]
