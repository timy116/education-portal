from django.conf.urls import url

from .views.index import index

urlpatterns = [
    url(r"^$", index, name="index"),
]
