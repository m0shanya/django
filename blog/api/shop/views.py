from rest_framework.exceptions import NotFound

from shop.models import Purchase, Product
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.users.serializers import UserModelSerializer, UserSerializer
from api.shop.serializers import ShopModelSerializer, PurchaseSerializer


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
