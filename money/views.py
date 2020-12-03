from django.shortcuts import redirect
from money.models import Spending, Asset, Transfer, SpendingCategory, Department
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views import generic
from money.forms import TodaySpendingsForm, PickupForm, TerminalForm, TransferForm, SpendingsForm, get_period
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from money.filters import SpendingFilter, TransfersFilter


# Spending views
class SpendingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'spendings.html'
    context_object_name = 'spendings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spendings = self.get_queryset()
        context['filter'] = SpendingFilter(
            self.request.GET,
            queryset=spendings,
        )
        sum = 0
        for spending in spendings:
            sum += spending.amount
        context['sum'] = sum
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return Spending.objects.filter(**filters)
        return Spending.objects.all()


class SpendingView(LoginRequiredMixin, generic.DetailView):
    model = Spending
    template_name = "spending.html"


class SpendingCreate(LoginRequiredMixin, CreateView):
    model = Spending
    form_class = SpendingsForm
    success_url = reverse_lazy('spendings')


class TodaySpendingCreate(LoginRequiredMixin, CreateView):  
    model = Spending
    form_class = TodaySpendingsForm
    success_url = reverse_lazy('today_sales_shop')



class SpendingUpdate(LoginRequiredMixin, UpdateView):
    model = Spending
    fields = '__all__'
    success_url = reverse_lazy('spendings')
    template_name = 'spending_update.html'

    def get_context_data(self, **kwargs):
        context = super(SpendingUpdate, self).get_context_data(**kwargs)
        context['spendings'] = Spending.objects.all()
        return context


class SpendingDelete(LoginRequiredMixin, DeleteView):
    model = Spending

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('spendings')
        return reverse_lazy('today_sales_shop')


# Assets views
class AssetsView(LoginRequiredMixin, generic.ListView):
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
        return Asset.objects.filter(is_active=True)

class NotActiveAssetsView(LoginRequiredMixin, generic.ListView):
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
        return Asset.objects.filter(is_active=False)


class AssetView(LoginRequiredMixin, generic.DetailView):
    model = Asset
    template_name = "asset.html"


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets')

    def get_context_data(self, **kwargs):
        context = super(AssetCreate, self).get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context


class AssetUpdate(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets')
    template_name = 'asset_update.html'

    def get_context_data(self, **kwargs):
        context = super(AssetUpdate, self).get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        return context


class AssetDelete(LoginRequiredMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets')


# Transfers views
class TransfersView(LoginRequiredMixin, generic.ListView):
    template_name = 'transfers.html'
    context_object_name = 'transfers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transfers = self.get_queryset()
        context['filter'] = TransfersFilter(
            self.request.GET,
            queryset=transfers,
        )
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return Transfer.objects.filter(**filters)
        return Transfer.objects.all()


class TransferView(LoginRequiredMixin, generic.DetailView):
    model = Transfer
    template_name = "transfer.html"


class TransferCreate(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    success_url = '/money/transfers/?period={}'.format(get_period().id)
    template_name = 'transfer_create.html'


class PickupCreate(LoginRequiredMixin, CreateView):  
    model = Transfer
    form_class = PickupForm
    success_url = reverse_lazy('today_sales_shop')


class TerminalCreate(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TerminalForm
    success_url = '/money/transfers/?period={}'.format(get_period().id)

    def form_valid(self, form):
        parameters = self.request.POST
        amount = float(parameters['amount'])
        spending_name = "Коммисия банка {}".format(
            datetime.date.today().strftime('%B'))
        try:
            spending = Spending.objects.get(name=spending_name)
        except ObjectDoesNotExist:
            asset = Asset.objects.get(name='Терминал')
            category = SpendingCategory.objects.get(name='Затраты')
            department = Department.objects.get(name='Магазин')
            period = get_period()
            spending = Spending(
                name=spending_name,
                amount=0,
                asset=asset,
                department=department,
                category=category,
                period=period
            )
        spending.amount += round((amount * 0.02), 2)
        spending.save()
        return super().form_valid(form)


@login_required
def terminal_from_spending(request, pk):
    spending = Spending.objects.get(id=pk)
    transfer_name = 'terminal {}'.format(spending.asset.name)
    terminal_asset_to = Asset.objects.get(name='Терминал')
    transfer = Transfer(
        name=transfer_name,
        asset_from=spending.asset,
        asset_to=terminal_asset_to,
        period=spending.period,
        amount=spending.amount,
    )
    transfer.save()
    commission_spending_name = "Коммисия банка {}".format(datetime.date.today().strftime('%B'))
    try:
        commission_spending = Spending.objects.get(
            name=commission_spending_name)
    except ObjectDoesNotExist:
        asset = Asset.objects.get(name='Терминал')
        category = SpendingCategory.objects.get(name='Затраты')
        department = Department.objects.get(name='Магазин')
        period = get_period()
        commission_spending = Spending(
            name=commission_spending_name,
            amount=0,
            asset=asset,
            department=department,
            category=category,
            period=period
        )
    commission_spending.amount += round((spending.amount * 0.02), 2)
    commission_spending.save()
    spending.delete()
    return redirect(reverse_lazy('spendings'))


class TransferUpdate(LoginRequiredMixin, UpdateView):
    model = Transfer
    fields = '__all__'
    success_url = '/money/transfers/?period={}'.format(get_period().id)
    template_name = 'transfer_update.html'


class TransferDelete(LoginRequiredMixin, DeleteView):
    model = Transfer

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('transfers')
        return reverse_lazy('today_sales_shop')
