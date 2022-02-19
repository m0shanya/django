import logging
import requests

import pandas as pd
import xml.etree.ElementTree as et

from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404, redirect
from lxml import etree

from shop.forms import ProductFiltersForm
from shop.models import Product, Purchase

logger = logging.getLogger(__name__)


def prod_list(request):
    products = Product.objects.all()
    filters_form = ProductFiltersForm(request.GET)

    if filters_form.is_valid():
        cost__gt = filters_form.cleaned_data["cost__gt"]
        if cost__gt:
            products = products.filter(cost__gt=cost__gt)

        cost__lt = filters_form.cleaned_data["cost__lt"]
        if cost__lt:
            products = products.filter(cost__lt=cost__lt)

        order_by = filters_form.cleaned_data["order_by"]
        if order_by:
            if order_by == "cost_asc":
                products = products.order_by("cost")
            if order_by == "cost_desc":
                products = products.order_by("-cost")
            if order_by == "max_count":
                products = products.annotate(total_count=Sum("purchases__count")).order_by(
                    "-total_count"
                )
            if order_by == "max_price":
                products = products.annotate(
                    total_cost=Sum("purchases__count") * F("cost")
                ).order_by("-total_cost")

    paginator = Paginator(products, 30)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "products/list.html", {"filters_form": filters_form, "products": products})


def product_details_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        if request.POST.get("count"):
            Purchase.objects.create(product=product, user=request.user, count=request.POST.get("count"))
            return redirect("product_details_view", product_id=product_id)
    return render(request, "products/details.html", {"product": product})


def currency_converter(request):
    url = 'https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=5c795253873b5e4ae9bd'
    params = {
        "USD_PHP": 51.440375
    }
    response = requests.get(url, params)

    tree = et.ElementTree(et.fromstring(response.text))
    root = tree.getroot()

    df_cols = ["numcode", "charcode", "nominal", "name", "value"]
    rows = []
    for node in root:
        s_numcode = node.find("NumCode").text if node is not None else None
        s_charcode = node.find("CharCode").text if node is not None else None
        s_nominal = node.find("Nominal").text if node is not None else None
        s_name = node.find("Name").text if node is not None else None
        s_value = node.find("Value").text if node is not None else None

        rows.append({"numcode": s_numcode,
                     "charcode": s_charcode, "nominal": s_nominal,
                     "name": s_name, "value": s_value})
    df = pd.DataFrame(rows, columns=df_cols)
    print(df.head())
