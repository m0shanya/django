from rest_framework import serializers

from shop.models import Purchase

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
