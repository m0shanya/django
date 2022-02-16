import logging
from pathlib import Path
from time import sleep

import requests
from django.conf import settings
from shop.models import Product
from shop.spiders import OmaSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from django_rq import job

logger = logging.getLogger(__name__)


@job
def run_products_update():
    logger.info("run_products_update is called")
    for _ in range(10):
        sleep(3)
        logger.info("run_products_update step")
    return "Finished"


def some_view_or_function():
    run_products_update.delay()


@job
def run_oma_spider():
    def crawler_results(signal, sender, item, response, spider):
        item["cost"] = int(item["cost"].split(",")[0])
        if item["image"]:
            response = requests.get(item["image"])
            if response.ok:
                path = Path(item["image"])
                open(settings.MEDIA_ROOT / path.name, "wb").write(response.content)
                item["image"] = path.name
        Product.objects.update_or_create(external_id=item["external_id"], defaults=item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(OmaSpider)
    process.start()
