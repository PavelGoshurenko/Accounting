import django_filters
from goods.models import Sale, Product


class SaleFilter(django_filters.FilterSet):

    class Meta:
        model = Sale
        fields = ['date', 'department', 'period']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'brand']


class SaleShortFilter(django_filters.FilterSet):

    class Meta:
        model = Sale
        fields = ['department', 'period']