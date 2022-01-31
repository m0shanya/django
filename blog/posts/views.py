import logging

from django.contrib.auth.models import User
from django.http import HttpResponse

from posts.models import Post

logger = logging.getLogger(__name__)


def posts_index(request):
    post_title = request.GET.get("title", "First title")
    posts = Post.objects.filter(title=post_title)
    return HttpResponse(posts)


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
