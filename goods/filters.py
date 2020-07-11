import django_filters
from goods.models import Sale
from django import forms


class SaleFilter(django_filters.FilterSet):

    class Meta:
        model = Sale
        fields = ['date', 'department']
