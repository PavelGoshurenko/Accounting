from rest_framework import serializers
from goods.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'shop_price',
            'internet_price',
            'purchase_price',
            'category',
            'brand',
        )


class InventoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'category',
            'brand',
        )
