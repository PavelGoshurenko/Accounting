from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from goods.models import Product, Incoming, Invoice, Sale, ProductBrand, ProductCategory, Inventory
from money.models import Department, Spending, Asset, Transfer, SpendingCategory, Period
from django.views.generic.base import TemplateView
from goods.forms import AddInvoiceForm
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import modelformset_factory
from goods.forms import SalesFromFileForm, InventoryForm
from goods.filters import SaleFilter, ProductFilter
import json
from django.forms import modelform_factory
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounting.settings import BASE_DIR
import os
from utilities.download import download
from django.db.models import F
from django.views.generic.dates import MonthArchiveView
from django.utils import timezone

# Products views


@login_required
def main(request):
    return HttpResponseRedirect('/products/all/?category=1&brand=')


class ProductsView(LoginRequiredMixin, generic.ListView):
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        context['filter'] = ProductFilter(
            self.request.GET,
            queryset=products,
        )
        sale_sum = 0
        purchase_sum = 0
        for product in products:
            sale_sum += product.quantity * product.shop_price
            purchase_sum += product.quantity * product.purchase_price
        context['sale_sum'] = sale_sum
        context['purchase_sum'] = purchase_sum
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            filters['is_active'] = True
            return Product.objects.filter(**filters)
        return Product.objects.filter(is_active=True)


class ProductsOrder(LoginRequiredMixin, generic.ListView):
    template_name = 'products_order.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        context['filter'] = ProductFilter(
            self.request.GET,
            queryset=products,
        )
        sale_sum = 0
        purchase_sum = 0
        for product in products:
            sale_sum += product.quantity * product.shop_price
            purchase_sum += product.quantity * product.purchase_price
        context['sale_sum'] = sale_sum
        context['purchase_sum'] = purchase_sum
        return context

    def get_queryset(self):
        f = F('min_quantity')
        products = Product.objects.filter(quantity__lt=f, is_active=True)
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return products.filter(**filters)
        return products


@login_required
def download_products(request):
    data = [[
        'Товар',
        'Остаток',
        'Цена интернет',
        'Цена магазин',
        'Цена покупки',
    ]]
    products = Product.objects.all()
    for product in products:
        row = [
            product.name,
            product.quantity,
            product.internet_price,
            product.shop_price,
            product.purchase_price,
        ]
        data.append(row)
    excel_file_name = 'goods.xlsx'
    response = download(excel_file_name, data)
    return response


@login_required
def download_products_order(request):
    data = [[
        'Товар',
        'Заказать',
        'Остаток',
        'Минимальное количество',
        'Цена покупки',
    ]]
    f = F('min_quantity')
    products = Product.objects.filter(quantity__lt=f, is_active=True)
    for product in products:
        row = [
            product.name,
            product.need_to_order(),
            product.quantity,
            product.min_quantity,
            product.purchase_price,
        ]
        data.append(row)
    excel_file_name = 'order.xlsx'
    response = download(excel_file_name, data)
    return response


class ProductView(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = "product.html"


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('index')
    template_name = 'product_update.html'


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('index')


# invoices views

@login_required
def new_invoice(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        new_invoice = Invoice(name=data['name'])
        new_invoice.save()
        new_incomings = data['incomings']
        for key, value in new_incomings.items():
            product = Product.objects.get(id=key)
            purchase_price = value['purchase_price']
            quantity = value['quantity']
            new_incoming = Incoming(
                product=product,
                invoice=new_invoice,
                purchase_price=purchase_price,
                quantity=quantity,
            )
            new_incoming.save()
        return redirect(reverse_lazy('invoices'))
        
    else:
        products = {}
        for product in Product.objects.filter(is_active=True):
            products[str(product.id)] = {
                'name': product.name,
                'purchase_price': product.purchase_price,
                'quantity': 0,
                'brand': product.brand.id if product.brand else None,
                'category': product.category.id if product.category else None,
                }
        js_data = json.dumps(products)
        filter_form = modelform_factory(
            Product,
            fields=('category', 'brand')
        )
        context = {'js_data': js_data, 'form': filter_form}
        return render(request, 'new_incoming.html', context)


class InvoicesView(LoginRequiredMixin, generic.ListView):
    template_name = 'invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all()


class InvoiceView(LoginRequiredMixin, generic.DetailView):
    model = Invoice
    template_name = "invoice.html"


class InvoiceCreate(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('invoices')


class InvoiceUpdate(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('invoices')
    template_name = 'invoice_update.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdate, self).get_context_data(**kwargs)
        invoice = self.get_object()
        incomings = invoice.incoming_set.all()
        context['incomings'] = incomings
        sum = 0
        for incoming in incomings:
            sum += incoming.quantity * incoming.purchase_price
        context['sum'] = sum
        return context

 
class InvoiceDelete(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices')


@login_required
def download_invoice(request, pk):
    data = [[
        'Товар',
        'Количество',
        'Цена интернет',
        'Цена магазин',
    ]]
    invoice = Invoice.objects.get(id=pk)
    incomings = invoice.incoming_set.all()
    for incoming in incomings:
        row = [
            incoming.product.name,
            incoming.quantity,
            incoming.product.internet_price,
            incoming.product.shop_price,
        ]
        data.append(row)
    excel_file_name = '{}.xlsx'.format(pk)
    response = download(excel_file_name, data)
    return response


# Incomings views


class IncomingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'incomings.html'
    context_object_name = 'incomings'

    def get_queryset(self):
        return Incoming.objects.all()


class IncomingView(LoginRequiredMixin, generic.DetailView):
    model = Incoming
    template_name = "incoming.html"


class IncomingCreate(LoginRequiredMixin, CreateView):
    model = Incoming
    fields = '__all__'
    success_url = reverse_lazy('incomings')



class IncomingUpdate(LoginRequiredMixin, UpdateView):
    model = Incoming
    fields = '__all__'
    success_url = reverse_lazy('incomings')
    template_name = 'incoming_update.html'


class IncomingDelete(LoginRequiredMixin, DeleteView):
    model = Incoming
    success_url = reverse_lazy('incomings')


# Sales views
class TodayShopSalesView(LoginRequiredMixin, generic.ListView):
    template_name = 'today_sales_shop.html'
    context_object_name = 'sales'

    def get_queryset(self):
        department = Department.objects.get(name='Магазин')
        return Sale.objects.filter(date=datetime.date.today(), department=department)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.get_queryset()
        sum = 0
        final_sum = sum
        for sale in sales:
            sum += sale.quantity * sale.price
        context['sum'] = sum
        asset_name = '{} {}'.format(datetime.date.today(), "Магазин")
        try:
            asset = Asset.objects.get(name=asset_name)
        except ObjectDoesNotExist:
            return context
        spendings = Spending.objects.filter(asset=asset)
        category = SpendingCategory.objects.get(name='Не отсортированные')
        spendings = spendings.filter(category=category)
        context['spendings'] = spendings
        spendings_sum = 0
        for spending in spendings:
            spendings_sum += spending.amount
        context['spendings_sum'] = spendings_sum
        pickups = Transfer.objects.filter(asset_to=asset)
        context['transfers'] = pickups
        pickups_sum = 0
        for pickup in pickups:
            pickups_sum += pickup.amount
        context['transfers_sum'] = pickups_sum
        final_sum = sum - spendings_sum + pickups_sum
        context['final_sum'] = final_sum
        return context


class TodayInternetSalesView(LoginRequiredMixin, generic.ListView):
    template_name = 'today_sales_internet.html'
    context_object_name = 'sales'

    def get_queryset(self):
        department = Department.objects.get(name='Интернет')
        return Sale.objects.filter(date=datetime.date.today(), department=department)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.get_queryset()
        sum = 0
        for sale in sales:
            sum += sale.quantity * sale.price
        context['sum'] = sum
        return context


class SalesView(LoginRequiredMixin, generic.ListView):
    template_name = 'sales.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.get_queryset()
        context['filter'] = SaleFilter(
            self.request.GET,
            queryset=sales,
        )
        sum = 0
        for sale in sales:
            sum += sale.quantity * sale.price
        context['sum'] = sum
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return Sale.objects.filter(**filters)
        return Sale.objects.all()


class SaleView(LoginRequiredMixin, generic.DetailView):
    model = Sale
    template_name = "sale.html"


class SaleCreate(LoginRequiredMixin, CreateView):
    model = Sale
    fields = '__all__'
    success_url = reverse_lazy('sales')


class SaleUpdate(LoginRequiredMixin, UpdateView):
    model = Sale
    fields = '__all__'
    success_url = '/products/sales/?date=&department=&period=1'
    template_name = 'sale_update.html'


class SaleDelete(LoginRequiredMixin, DeleteView):
    model = Sale
    success_url = reverse_lazy('sales')

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('sales')
        return reverse_lazy('index')


@login_required
def add_sales_shop(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        date = datetime.date.today()
        department = Department.objects.get(name='Магазин')
        manager = request.user
        period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
        try:
            period = Period.objects.get(name=period_name)
        except ObjectDoesNotExist:
            period = Period(name=period_name)
            period.save()
        new_sales = data['sales']
        for key, value in new_sales.items():
            product = Product.objects.get(id=key)
            price = value['shop_price'] - value['discount'] / value['quantity']
            quantity = value['quantity']
            new_sale = Sale(
                date=date,
                manager=manager,
                price=price,
                product=product,
                department=department,
                quantity=quantity,
                purchase_price=product.purchase_price,
                period=period
            )
            new_sale.save()
        return redirect(reverse_lazy('sales'))
        
    else:
        products = {}
        for product in Product.objects.filter(is_active=True):
            products[str(product.id)] = {
                'name': product.name,
                'shop_price': product.shop_price,
                'quantity': 0,
                'discount': 0,
                'brand': product.brand.id if product.brand else None,
                'category': product.category.id if product.category else None,
                }
        js_data = json.dumps(products)
        filter_form = modelform_factory(
            Product,
            fields=('category', 'brand')
        )
        context = {'js_data': js_data, 'form': filter_form}
        return render(request, 'add_sales.html', context)


@login_required
def add_sales_internet(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        date = datetime.date.today()
        department = Department.objects.get(name='Интернет')
        manager = request.user
        period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
        try:
            period = Period.objects.get(name=period_name)
        except ObjectDoesNotExist:
            period = Period(name=period_name)
            period.save()
        new_sales = data['sales']
        for key, value in new_sales.items():
            product = Product.objects.get(id=key)
            price = value['shop_price'] - value['discount'] / value['quantity']
            quantity = value['quantity']
            new_sale = Sale(
                date=date,
                manager=manager,
                price=price,
                product=product,
                department=department,
                quantity=quantity,
                purchase_price=product.purchase_price,
                period=period
            )
            new_sale.save()
        return redirect(reverse_lazy('sales'))
        
    else:
        products = {}
        for product in Product.objects.filter(is_active=True):
            products[str(product.id)] = {
                'name': product.name,
                'shop_price': product.internet_price,
                'quantity': 0,
                'discount': 0,
                'brand': product.brand.id if product.brand else None,
                'category': product.category.id if product.category else None,
                }
        js_data = json.dumps(products)
        filter_form = modelform_factory(
            Product,
            fields=('category', 'brand')
        )
        context = {'js_data': js_data, 'form': filter_form}
        return render(request, 'add_sales.html', context)


# inventories views
@login_required
def add_inventories(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        date = datetime.date.today()
        new_inventories = data['inventories']
        for key, value in new_inventories.items():
            product = Product.objects.get(id=key)
            new_inventory = Inventory(
                date=date,
                product=product,
                supposed_quantity=product.quantity,
            )
            new_inventory.save()
        return redirect(reverse_lazy('sales'))
        
    else:
        products = {}
        for product in Product.objects.filter(is_active=True):
            products[str(product.id)] = {
                'name': product.name,
                'added': False,
                'brand': product.brand.id if product.brand else None,
                'category': product.category.id if product.category else None,
                }
        js_data = json.dumps(products)
        filter_form = modelform_factory(
            Product,
            fields=('category', 'brand')
        )
        context = {'js_data': js_data, 'form': filter_form}
        return render(request, 'add_inventories.html', context)


@login_required
def inventories(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        new_inventories = data['inventories']
        for key, new_inventory in new_inventories.items():
            old_inventory = Inventory.objects.get(id=key)
            new_fact_quantity = new_inventory['fact_quantity']
            if new_fact_quantity != old_inventory.fact_quantity:
                old_inventory.fact_quantity = new_fact_quantity
                old_inventory.save()
        return redirect(reverse_lazy('inventories_result'))
        
    else:
        inventories = {}
        for inventory in Inventory.objects.filter(confirmed=False):
            brand = '' if inventory.product.brand is None else inventory.product.brand.name
            inventories[str(inventory.id)] = {
                'name': inventory.product.name,
                'brand': brand,
                'supposed_quantity': inventory.supposed_quantity,
                'fact_quantity': inventory.fact_quantity,
                }
        js_data = json.dumps(inventories)
        context = {'js_data': js_data}
        return render(request, 'inventories.html', context)


@login_required
def confirm_inventories(request):
    inventories = Inventory.objects.filter(confirmed=False)
    date = datetime.date.today()
    period_name = datetime.datetime.strftime(timezone.now(), '%B %Y')
    try:
        period = Period.objects.get(name=period_name)
    except ObjectDoesNotExist:
        period = Period(name=period_name)
        period.save()
    for inventory in inventories:
        shortage = inventory.supposed_quantity - inventory.fact_quantity
        if shortage:
            product = inventory.product
            sale = Sale(
                manager=User.objects.get(username='fisher'),
                department=Department.objects.get(name='Офис'),
                price=product.internet_price,
                purchase_price=product.purchase_price,
                product=product,
                quantity=shortage,
                date=date,
                period=period
            )
            sale.save()
        inventory.confirmed = True
        inventory.save()
    return redirect('inventories')


class InventoriesResult(LoginRequiredMixin, generic.ListView):
    template_name = 'inventories_result.html'
    context_object_name = 'inventories'

    def get_queryset(self):
        queryset = Inventory.objects.filter(confirmed=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventories = self.get_queryset()
        sum = 0
        for inventory in inventories:
            sum += inventory.cost()
        context['sum'] = sum
        return context
