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

    def perform_create(self, serializer):
        user = User(
            username=serializer.validated_data["email"],
            email=serializer.validated_data["email"],
        )
        product = Product(
            id=serializer.validated_data["product"]
        )
        count = serializer.validated_data["count"]
        Purchase.objects.create(user=user, product=product, count=count)