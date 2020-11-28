import django_filters
from money.models import Spending, Transfer
from django import forms


class SpendingFilter(django_filters.FilterSet):

    class Meta:
        model = Spending
        fields = ['category', 'department', 'period']


class TransfersFilter(django_filters.FilterSet):

    class Meta:
        model = Transfer
        fields = ['period']
