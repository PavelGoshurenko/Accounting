from django import forms
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.forms.models import modelformset_factory
from goods.models import Product, Incoming
from money.models import Spending, SpendingCategory, Asset, Transfer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import datetime

def get_asset(department):
    asset_name = '{} {}'.format(datetime.date.today(), department)
    try:
        asset = Asset.objects.get(name=asset_name)
    except ObjectDoesNotExist:
        asset = Asset(name=asset_name, amount=0)
        asset.save()
    return asset


def get_name():
    return 'terminal {}'.format(datetime.date.today())


class TodaySpendingsForm (forms.ModelForm):
    category = forms.ModelChoiceField(
        initial=SpendingCategory.objects.get(name='Не отсортированные'),
        queryset=SpendingCategory.objects.all(),
        disabled=True,
        label='Категория',
        widget=forms.HiddenInput,
        )
    asset = forms.ModelChoiceField(
        initial=get_asset("Магазин"),
        queryset=Asset.objects.all(),
        disabled=True,
        label='Источник',
        widget=forms.HiddenInput,
    )
    # а не поломается ли сейл если при первой продаже уже будет ассет
    
    class Meta:
        model = Spending
        fields = ('name', 'amount', 'category', 'asset')


class PickupForm (forms.ModelForm):
    asset_from = forms.ModelChoiceField(
        initial=get_asset('Интернет'),
        disabled=True,
        queryset=Asset.objects.all(),
        label='Из кассы:',
        widget=forms.HiddenInput,
    )
    asset_to = forms.ModelChoiceField(
        initial=get_asset('Магазин'),
        disabled=True,
        queryset=Asset.objects.filter(is_active=True),
        label='В кассу:',
        widget=forms.HiddenInput,
    )

    class Meta:
        model = Transfer
        fields = ('amount', 'name', 'asset_from', 'asset_to')
        labels = {
            'name': 'Примечание',
        }


class TerminalForm (forms.ModelForm):
    asset_from = forms.ModelChoiceField(
        queryset=Asset.objects.filter(is_active=True),
        label='Откуда:'
    )
    asset_to = forms.ModelChoiceField(
        initial=Asset.objects.get(name="Терминал"),
        disabled=True,
        queryset=Asset.objects.filter(is_active=True),
        label='Куда:'
    )
    name = forms.CharField(
        label='Примечание:',
        initial=get_name()
    )
    
    class Meta:
        model = Transfer
        fields = ('amount', 'name', 'asset_from', 'asset_to')
        labels = {
            'name': 'Примечание',
        }


class TransferForm (forms.ModelForm):
    asset_from = forms.ModelChoiceField(
        queryset=Asset.objects.filter(is_active=True),
        label='Из актива:'
    )
    asset_to = forms.ModelChoiceField(
        queryset=Asset.objects.filter(is_active=True),
        label='В актив:'
    )
    
    class Meta:
        model = Transfer
        fields = ('amount', 'name', 'asset_from', 'asset_to')

