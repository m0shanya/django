import logging
from pathlib import Path
from time import sleep
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import xml.etree.ElementTree as et
from dateutil.parser import parse

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


@job
def currency_converter():
    url = 'https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=5c795253873b5e4ae9bd'
    params = {
        "USD_PHP": 51.440375
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get the last updated time
    price_datetime = parse(soup.find_all("span", attrs={"class": "ratesTimestamp"})[1].text)
    # get the exchange rates tables
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            # for each row in the table
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                # get the exchange rate
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate
    return price_datetime, exchange_rates
