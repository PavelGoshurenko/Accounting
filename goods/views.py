from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from goods.models import Product, Incoming, Invoice, Sale
from django.views.generic.base import TemplateView
import openpyxl
from goods.forms import AddInvoiceForm
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory

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
        context['who'] = sheet["A44"].value
        return context


# invoices views
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


# Incomings views
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

    def get_queryset(self):
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