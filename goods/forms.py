from django import forms
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.forms.models import modelformset_factory
from goods.models import Product, Incoming
from django.shortcuts import get_object_or_404


class AddInvoiceForm(forms.Form):
    invoice_name = forms.CharField(help_text="Имя накладной")
