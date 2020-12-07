from rest_framework import generics
from goods.serializer import ProductSerializer
from goods.models import Product


class ProductApi(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


