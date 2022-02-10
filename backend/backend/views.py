from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "index.html")


def logout(request):
    django_logout(request)

    return HttpResponseRedirect(reverse("index"))
