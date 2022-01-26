import logging
from django.http import HttpResponse

from posts.models import Post

logger = logging.getLogger(__name__)


def posts_index(request):
    post_title = request.GET.get("title", "First title")
    posts = Post.objects.filter(author__username=post_title)
    return HttpResponse(posts)
