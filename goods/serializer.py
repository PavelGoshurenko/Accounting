from rest_framework import serializers
from goods.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'internet_price',
            'category',
            'brand',
        )
