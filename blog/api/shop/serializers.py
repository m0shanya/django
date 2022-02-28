from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop.models import Purchase, Product, ORDER_BY_CHOICES


class ShopModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            "id",
            "count",
            "user_id",
            "product_id",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class PurchaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    product = serializers.IntegerField()
    count = serializers.IntegerField()


class PurchaseCreateSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1)


class ProductModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "cost", "external_id", "description", "image", "link", "status"]


class ProductFiltersSerializer(serializers.Serializer):
    cost__gt = serializers.IntegerField(min_value=0, label="Cost Min", required=False)
    cost__lt = serializers.IntegerField(min_value=0, label="Cost Max", required=False)
    order_by = serializers.ChoiceField(choices=ORDER_BY_CHOICES, required=False)

    def validate(self, attrs):
        cleaned_data = super().validate(attrs)
        cost__gt = cleaned_data.get("cost__gt")
        cost__lt = cleaned_data.get("cost__lt")
        if cost__gt and cost__lt and cost__gt > cost__lt:
            raise ValidationError("Min price can't be greater than Max price")
        return attrs

