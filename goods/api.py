from rest_framework import generics
from goods.serializer import ProductSerializer, InventoryAddSerializer
from goods.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductApi(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductInvApi(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = InventoryAddSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
