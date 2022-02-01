import logging

from django.shortcuts import render

from blog.forms import RegisterForm

logger = logging.getLogger(__name__)


def register(request):
    form = RegisterForm()
    return render(request, "register.html", {"form": form})
