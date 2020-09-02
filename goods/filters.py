import django_filters
from goods.models import Sale, Product
from django import forms


class SaleFilter(django_filters.FilterSet):

    class Meta:
        model = Sale
        fields = ['date', 'department', 'period']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'brand']