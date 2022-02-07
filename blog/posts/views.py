import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.forms import AddPostForm, LoginForm
from posts.models import Post

logger = logging.getLogger(__name__)


def posts_index(request):
    posts = []
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                logger.info(form.cleaned_data)
                post = Post.objects.create(author=request.user, **form.cleaned_data)
                post.save()
                return redirect('/')
        else:
            form = AddPostForm()
        posts = Post.objects.order_by("-created_at")
        logger.info(f"Posts of all users")
        return render(request, "posts_list.html", {"posts": posts, "form": form})
    else:
        logger.info(request, f"You don't logIn")
        return redirect('/login/')


def posts_index_user(request):
    user = User.objects.get(id=request.GET.get("author_id", 1))
    posts = Post.objects.filter(author=user)
    out = ""
    for post in posts:
        out += f"<div style='border: 1px solid black'>"
        out += f"<h2> Author: {post.author}</h2><br>"
        out += f"<h2> Title: {post.title}</h2><br>"
        out += f"<h2> Image: {post.image}</h2><br>"
        out += f"<h2> Text: {post.text}</h2><br>"
        out += f"<div> Created at: {post.created_at}</h2><br>"
        out += f"</div>"
    return HttpResponse(out)


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                logger.info(form.cleaned_data)
                post = Post.objects.create(author=request.user, **form.cleaned_data)
                post.save()
                return redirect('/', )
        else:
            form = AddPostForm()
        return render(request, 'add_post.html', {'form': form})
    else:
        return redirect('/login/', )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(request, f"Authenticated successfully")
                    return redirect('/', )
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/', )
    return render(request, "logout.html",)
