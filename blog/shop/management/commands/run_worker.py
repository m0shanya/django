import logging

from django.core.management.base import BaseCommand

from shop.tasks import some_view_or_function

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run worker"

    def handle(self, *args, **options):
        some_view_or_function()
