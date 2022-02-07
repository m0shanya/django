import logging
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from posts.models import Post


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Print posts"

    def handle(self, *args, **options):
        with open(settings.BASE_DIR / "posts.csv", "w") as file:
            writer = csv.writer(file)
            for post in Post.objects.all():
                writer.writerow([post.id, post.title])
        """for posts in Post.objects.all():
            logger.info(posts)"""
