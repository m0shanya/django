from django.db.models import Sum, F
from rest_framework.exceptions import NotFound

from shop.models import Purchase, Product
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.shop.serializers import ShopModelSerializer, ProductModelSerializer, ProductFiltersSerializer


class PurchaseViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that allows get user.
    """

    queryset = Purchase.objects.all()
    serializer_class = ShopModelSerializer
    permission_classes = [IsAuthenticated]


class PurchaseCreateView(CreateAPIView):
    """
    API endpoint that allows to create users.
    """

    serializer_class = ShopModelSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        product_id = kwargs.get("product_id")
        if not product_id:
            raise NotFound
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound
        serializer.is_valid(data=request.POST)
        Purchase.objects.create(user=request.user, product=product, count=serializer.validated_data["count"])
        return Response(status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """

    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        serializer = ProductFiltersSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        cost__gt = serializer.validated_data.get("cost__gt")
        if cost__gt is not None:
            queryset = queryset.filter(cost__gt=cost__gt)

        cost__lt = serializer.validated_data.get("cost__lt")
        if cost__lt is not None:
            queryset = queryset.filter(cost__lt=cost__lt)

        order_by = serializer.validated_data.get("order_by")
        if order_by:
            if order_by == "cost_asc":
                queryset = queryset.order_by("cost")
            if order_by == "cost_desc":
                queryset = queryset.order_by("-cost")
            if order_by == "max_count":
                queryset = queryset.annotate(
                    total_count=Sum("purchases__count")
                ).order_by("-total_count")
            if order_by == "max_price":
                queryset = queryset.annotate(
                    total_cost=Sum("purchases__count") * F("cost")
                ).order_by("-total_cost")

        return queryset
