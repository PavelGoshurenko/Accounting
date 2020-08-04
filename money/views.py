from django.shortcuts import render, get_object_or_404
from money.models import Spending, Asset, Transfer, SpendingCategory, Department
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from money.forms import TodaySpendingsForm, PickupForm, TerminalForm
from django.core.exceptions import ObjectDoesNotExist
import datetime


# Spending views
class SpendingsView(generic.ListView):
    template_name = 'spendings.html'
    context_object_name = 'spendings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context

    def get_queryset(self):
        return Spending.objects.all()


class SpendingView(generic.DetailView):
    model = Spending
    template_name = "spending.html"


class SpendingCreate(CreateView):
    model = Spending
    fields = '__all__'
    success_url = reverse_lazy('spendings')

    def get_context_data(self, **kwargs):
        context = super(SpendingCreate, self).get_context_data(**kwargs)
        context['spendings'] = Spending.objects.all()
        return context


class TodaySpendingCreate(CreateView):  
    model = Spending
    form_class = TodaySpendingsForm
    success_url = reverse_lazy('today_sales_shop')



class SpendingUpdate(UpdateView):
    model = Spending
    fields = '__all__'
    success_url = reverse_lazy('spendings')
    template_name = 'spending_update.html'

    def get_context_data(self, **kwargs):
        context = super(SpendingUpdate, self).get_context_data(**kwargs)
        context['spendings'] = Spending.objects.all()
        return context


class SpendingDelete(DeleteView):
    model = Spending
    success_url = reverse_lazy('spendings')


# Assets views
class AssetsView(generic.ListView):
    template_name = 'assets.html'
    context_object_name = 'assets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assets = self.get_queryset()
        sum = 0
        for asset in assets:
            sum += asset.amount
        context['sum'] = sum
        return context

    def get_queryset(self):
        return Asset.objects.all()


class AssetView(generic.DetailView):
    model = Asset
    template_name = "asset.html"


class AssetCreate(CreateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets')

    def get_context_data(self, **kwargs):
        context = super(AssetCreate, self).get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context


class AssetUpdate(UpdateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets')
    template_name = 'asset_update.html'

    def get_context_data(self, **kwargs):
        context = super(AssetUpdate, self).get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context


class AssetDelete(DeleteView):
    model = Asset
    success_url = reverse_lazy('assets')


# Transfers views
class TransfersView(generic.ListView):
    template_name = 'transfers.html'
    context_object_name = 'transfers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context

    def get_queryset(self):
        return Transfer.objects.all()


class TransferView(generic.DetailView):
    model = Transfer
    template_name = "transfer.html"


class TransferCreate(CreateView):
    model = Transfer
    fields = '__all__'
    success_url = reverse_lazy('transfers')

    def get_context_data(self, **kwargs):
        context = super(TransferCreate, self).get_context_data(**kwargs)
        context['transfers'] = Transfer.objects.all()
        return context

class PickupCreate(CreateView):  
    model = Transfer
    form_class = PickupForm
    success_url = reverse_lazy('today_sales_shop')

class TerminalCreate(CreateView):
    model = Transfer
    form_class = TerminalForm
    success_url = reverse_lazy('transfers')

    def form_valid(self, form):
        parameters = self.request.POST
        amount = float(parameters['amount'])
        spending_name = "Коммисия банка {}".format(datetime.date.today().strftime('%B'))
        try:
            spending = Spending.objects.get(name=spending_name)
        except ObjectDoesNotExist:
            asset = Asset.objects.get(name='Терминал')
            category = SpendingCategory.objects.get(name='Затраты')
            department = Department.objects.get(name='Магазин')
            spending = Spending(
                name=spending_name,
                amount=0,
                asset=asset,
                department=department,
                category=category
            )
        spending.amount += round((amount * 0.02), 2)
        spending.save()
        return super().form_valid(form)

class TransferUpdate(UpdateView):
    model = Transfer
    fields = '__all__'
    success_url = reverse_lazy('transfers')
    template_name = 'transfer_update.html'

    def get_context_data(self, **kwargs):
        context = super(TransferUpdate, self).get_context_data(**kwargs)
        context['transfers'] = Transfer.objects.all()
        return context


class TransferDelete(DeleteView):
    model = Transfer
    success_url = reverse_lazy('transfers')