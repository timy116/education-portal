from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def register(request):
    if request.user.is_authenticated:
        ...

    return render(request, "register.html")
