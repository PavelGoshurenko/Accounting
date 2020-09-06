import django_filters
from money.models import Spending
from django import forms


class SpendingFilter(django_filters.FilterSet):

    class Meta:
        model = Spending
        fields = ['category', 'department', 'period']
