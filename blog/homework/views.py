import logging
from django.http import HttpResponse
from homework.models import Profile
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def homework_index(request):
    value = request.GET.get("get-key-1")
    value and logger.info(f"get-key-1 = {value}")
    value = request.GET.get("get-key-2")
    value and logger.info(f"get-key-2 = {value}")
    value = request.GET.get("get-key-3")
    value and logger.info(f"get-key-3 = {value}")

    # Processing POST params
    value = request.POST.get("post-key-1")
    value and logger.info(f"post-key-1 = {value}")
    value = request.POST.get("post-key-2")
    value and logger.info(f"post-key-2 = {value}")
    value = request.POST.get("post-key-3")
    value and logger.info(f"post-key-3 = {value}")

    return HttpResponse("Homework index view")


def profile_index(request):
    user = User.objects.get(id=request.GET.get("author_id", 1))
    profiles = Profile.objects.filter(user=user)
    out = ""
    for profile in profiles:
        out += f"<div style='border: 1px solid black'>"
        out += f"<h2> Author: {profile.user}</h2><br>"
        out += f"<h2> Age: {profile.age}</h2><br>"
        out += f"<div> Created at: {profile.created_at}</h2><br>"
        out += f"</div>"
    return HttpResponse(out)
