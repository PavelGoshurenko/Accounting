from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from goods.models import Product, Incoming, Invoice, Sale
from django.views.generic.base import TemplateView
import openpyxl
from goods.forms import AddInvoiceForm
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from goods.forms import SalesFromFileForm
from goods.filters import SaleFilter
import json

# Products views


class ProductsView(generic.ListView):
    template_name = 'products.html'
    context_object_name = 'products'

    def get_queryset(self):
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
        wb = openpyxl.load_workbook('1.xlsx')
        sheet = wb.active
        i = 3
        while i < 2350:
            if sheet['A{}'.format(i)].value and sheet['I{}'.format(i)].value:
                new_product = Product(
                    name=sheet['A{}'.format(i)].value,
                    shop_price=sheet['I{}'.format(i)].value,
                    purchase_price=sheet['L{}'.format(i)].value,
                    internet_price=sheet['J{}'.format(i)].value,
                    quantity=sheet['G{}'.format(i)].value,
                    category=None,
                    brand=None
                    )
                new_product.save()
            i += 1
        context['who'] = sheet["A44"].value
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
                }
        js_data = json.dumps(products)
        context = {'js_data': js_data}
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
        context['invoices'] = Invoice.objects.all()
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
