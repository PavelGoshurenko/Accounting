from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from goods.models import Product, Incoming, Invoice, Sale, ProductBrand, ProductCategory
from money.models import Department, Spending, Asset, Transfer
from django.views.generic.base import TemplateView
import openpyxl
from goods.forms import AddInvoiceForm
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from goods.forms import SalesFromFileForm
from goods.filters import SaleFilter, ProductFilter
import json
from django.forms import modelform_factory
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Products views


class ProductsView(generic.ListView):
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
            return Product.objects.filter(**filters)
        return Product.objects.all()


class ProductView(generic.DetailView):
    model = Product
    template_name = "product.html"


class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')
    template_name = 'product_update.html'

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('products')


class AddProductsView(TemplateView):

    template_name = "add_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wb = openpyxl.load_workbook('products.xlsx')
        sheet = wb.active
        i = 3
        while i < 2350:
            if sheet['A{}'.format(i)].value and sheet['C{}'.format(i)].value:
                if sheet['F{}'.format(i)].value:
                    category = ProductCategory.objects.get(name=sheet['F{}'.format(i)].value)
                else:
                    category = None
                if sheet['G{}'.format(i)].value:
                    brand = ProductBrand.objects.get(name=sheet['G{}'.format(i)].value)
                else:
                    brand = None
                new_product = Product(
                    name=sheet['A{}'.format(i)].value,
                    shop_price=sheet['C{}'.format(i)].value,
                    purchase_price=sheet['E{}'.format(i)].value,
                    internet_price=sheet['D{}'.format(i)].value,
                    quantity=sheet['B{}'.format(i)].value,
                    category=category,
                    brand=brand
                    )
                new_product.save()
            i += 1
        return context


# invoices views

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
        for product in Product.objects.all():
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


class InvoicesView(generic.ListView):
    template_name = 'invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all()


class InvoiceView(generic.DetailView):
    model = Invoice
    template_name = "invoice.html"


class InvoiceCreate(CreateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('invoices')

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreate, self).get_context_data(**kwargs)
        context['invoices'] = Invoice.objects.all()
        return context


class InvoiceUpdate(UpdateView):
    model = Invoice
    fields = '__all__'
    success_url = reverse_lazy('invoices')
    template_name = 'invoice_update.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdate, self).get_context_data(**kwargs)
        invoice = self.get_object()
        context['incomings'] = invoice.incoming_set.all()
        return context


class InvoiceDelete(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices')


# Incomings views
def add_incomings(request):
    IncomingFormSet = modelformset_factory(Incoming, exclude=('id',), extra=10)
    if request.method == 'POST':
        formset = IncomingFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = IncomingFormSet()
    return render(request, 'add_incomings.html', {'formset': formset})


class IncomingsView(generic.ListView):
    template_name = 'incomings.html'
    context_object_name = 'incomings'

    def get_queryset(self):
        return Incoming.objects.all()


class IncomingView(generic.DetailView):
    model = Incoming
    template_name = "incoming.html"



class IncomingCreate(CreateView):
    model = Incoming
    fields = '__all__'
    success_url = reverse_lazy('incomings')

    def get_context_data(self, **kwargs):
        context = super(IncomingCreate, self).get_context_data(**kwargs)
        context['incomings'] = Incoming.objects.all()
        return context


class IncomingUpdate(UpdateView):
    model = Incoming
    fields = '__all__'
    success_url = reverse_lazy('incomings')
    template_name = 'incoming_update.html'

    def get_context_data(self, **kwargs):
        context = super(IncomingUpdate, self).get_context_data(**kwargs)
        context['incomings'] = Incoming.objects.all()
        return context


class IncomingDelete(DeleteView):
    model = Incoming
    success_url = reverse_lazy('incomings')


# Sales views
class TodayShopSalesView(generic.ListView):
    template_name = 'today_sales_shop.html'
    context_object_name = 'sales'

    def get_queryset(self):
        department = Department.objects.get(name='Магазин')
        return Sale.objects.filter(date=datetime.date.today(), department=department)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.get_queryset()
        sum = 0
        for sale in sales:
            sum += sale.quantity * sale.price
        context['sum'] = sum
        asset_name = '{} {}'.format(datetime.date.today(), "Магазин")
        try:
            asset = Asset.objects.get(name=asset_name)
        except ObjectDoesNotExist:
            return context
        spendings = Spending.objects.filter(asset=asset)
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
        return context


class TodayInternetSalesView(generic.ListView):
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


class SalesView(generic.ListView):
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


class SaleView(generic.DetailView):
    model = Sale
    template_name = "sale.html"


class SaleCreate(CreateView):
    model = Sale
    fields = '__all__'
    success_url = reverse_lazy('sales')

    def get_context_data(self, **kwargs):
        context = super(SaleCreate, self).get_context_data(**kwargs)
        context['sales'] = Sale.objects.all()
        return context


class SaleUpdate(UpdateView):
    model = Sale
    fields = '__all__'
    success_url = reverse_lazy('sales')
    template_name = 'sale_update.html'

    def get_context_data(self, **kwargs):
        context = super(SaleUpdate, self).get_context_data(**kwargs)
        context['sales'] = Sale.objects.all()
        return context


class SaleDelete(DeleteView):
    model = Sale
    success_url = reverse_lazy('sales')


def get_sales_from_file():
    wb = openpyxl.load_workbook('1.xlsx')
    sheet = wb.active
    sales = []
    cost = 0
    i = 3
    while i < 2350:
        if sheet['A{}'.format(i)].value and sheet['B{}'.format(i)].value:
            sale = {}
            sale['product_name'] = sheet['A{}'.format(i)].value
            sale['quantity'] = sheet['B{}'.format(i)].value
            sale['price'] = sheet['C{}'.format(i)].value
            discount = sheet['E{}'.format(i)].value
            if discount is None:
                discount = 0
            sale['discount'] = discount
            sale['cost'] = sale['quantity'] * sale['price'] - sale['discount']
            cost += sale['cost']
            sales.append(sale)
        i += 1
    return (sales, cost)


def sales_from_file(request):
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = SalesFromFileForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            sales, cost = get_sales_from_file()
            date = form.cleaned_data['date']
            manager = form.cleaned_data['manager']
            department = form.cleaned_data['department']
            for sale in sales:
                product = Product.objects.get(name=sale['product_name'])
                if department.name == 'Магазин':
                    price = product.shop_price
                elif department.name == 'Интернет':
                    price = product.internet_price
                new_sale = Sale(
                    date=date,
                    manager=manager,
                    department=department,
                    price=price - sale['discount'] / sale['quantity'],
                    product=product,
                    quantity=sale['quantity']
                )
                new_sale.save()
            return HttpResponseRedirect(reverse('sales'))

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        form = SalesFromFileForm()
        sales, cost = get_sales_from_file()
        
    return render(
        request,
        'sales_from_file.html',
        context={'sales': sales, 'cost': cost, 'form': form}
        )


def add_sales_shop(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        date = datetime.date.today()
        department = Department.objects.get(name='Магазин')
        manager = request.user
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
                purchase_price=product.purchase_price
            )
            new_sale.save()
        return redirect(reverse_lazy('sales'))
        
    else:
        products = {}
        for product in Product.objects.all():
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


def add_sales_internet(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        date = datetime.date.today()
        department = Department.objects.get(name='Интернет')
        manager = request.user
        # new_invoice = Invoice(name=data['name'])
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
            )
            new_sale.save()
        return redirect(reverse_lazy('sales'))
        
    else:
        products = {}
        for product in Product.objects.all():
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
