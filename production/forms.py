from django import forms
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.forms.models import modelformset_factory
from goods.models import Product, Incoming
from production.models import Manufacturing, Proportion
from django.shortcuts import get_object_or_404


class ManufacturingForm (forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(proportion__quantity__gt=0).distinct())
    
    class Meta:
        model = Manufacturing
        fields = ('product', 'quantity', 'created_at')