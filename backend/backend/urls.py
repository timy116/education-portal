from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import index, logout

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^logout/$", logout, name="logout"),
    path('admin/', admin.site.urls),
    url(r"^", include("apps.portal.url.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls'))
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
