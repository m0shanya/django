import logging

from django.core.management.base import BaseCommand

from shop.tasks import currency_converter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run currency converter"

    def handle(self, *args, **options):
        currency_converter.delay()
