import logging

from django.shortcuts import render, redirect

from blog.forms import RegisterForm

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Process validated data
            logger.info(form.cleaned_data)
            user = User(email=form.cleaned_data['email'])
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
