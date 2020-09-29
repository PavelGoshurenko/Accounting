from django import forms
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.forms.models import modelformset_factory
from goods.models import Product, Incoming, Inventory, Invoice, Task
from money.models import Department
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from utilities.get_period import get_period


class AddInvoiceForm(forms.Form):
    invoice_name = forms.CharField(help_text="Имя накладной")

class SalesFromFileForm(forms.Form):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    manager = forms.ModelChoiceField(queryset=User.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())


class InventoryForm (forms.ModelForm):
    product = forms.ModelChoiceField(
        disabled=True,
        queryset=Product.objects.all(),
    )
    supposed_quantity = forms.FloatField(
        disabled=True,
    )

    class Meta:
        model = Inventory
        fields = ('product', 'supposed_quantity', 'fact_quantity')
        labels = {
            'fact_quantity': '',
        }
