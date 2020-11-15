from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from production.models import Ingredient, IngredientIncoming, IngredientInvoice, Manufacturing, IngredientCategory
from django.views.generic.base import TemplateView
import openpyxl
from production.filters import IngredientFilter
import json
from django.forms import modelform_factory
from production.forms import ManufacturingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounting.settings import BASE_DIR
import os

# Ingredient views 


class IngredientsView(LoginRequiredMixin, generic.ListView):
    template_name = 'ingredients.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = self.get_queryset()
        context['filter'] = IngredientFilter(
            self.request.GET,
            queryset=self.get_queryset(),
        )
        sum = 0
        for ingredient in ingredients:
            sum += ingredient.quantity * ingredient.purchase_price
        context['sum'] = sum
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return Ingredient.objects.filter(**filters)
        return Ingredient.objects.all()


class IngredientView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    template_name = "ingredient.html"


class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('ingredients')

    def get_context_data(self, **kwargs):
        context = super(IngredientCreate, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('ingredients')
    template_name = 'ingredient_update.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientUpdate, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context


class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredients')


class AddIngredientsView(LoginRequiredMixin, TemplateView):

    template_name = "add_ingredients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wb = openpyxl.load_workbook(os.path.join(BASE_DIR, 'goods/static/xlsx/ingredients.xlsx'))
        sheet = wb.active
        i = 2
        while i < 242:
            if sheet['A{}'.format(i)].value:
                new_ingredient = Ingredient(
                    name=sheet['A{}'.format(i)].value,
                    purchase_price=sheet['C{}'.format(i)].value,
                    quantity=sheet['D{}'.format(i)].value,
                    category=IngredientCategory.objects.get(name=sheet['B{}'.format(i)].value),
                    )
                new_ingredient.save()
            i += 1
        return context


# invoices views
@login_required
def new_ingredient_invoice(request):
    if request.method == 'POST':
        data = json.loads(request.POST['request'])
        new_invoice = IngredientInvoice(name=data['name'])
        new_invoice.save()
        new_incomings = data['incomings']
        for key, value in new_incomings.items():
            ingredient = Ingredient.objects.get(id=key)
            purchase_price = value['purchase_price']
            quantity = value['quantity']
            new_incoming = IngredientIncoming(
                ingredient=ingredient,
                invoice=new_invoice,
                purchase_price=purchase_price,
                quantity=quantity,
            )
            new_incoming.save()
        return redirect(reverse_lazy('ingredient_invoices'))
        
    else:
        ingredients = {}
        for ingredient in Ingredient.objects.all():
            ingredients[str(ingredient.id)] = {
                'name': ingredient.name,
                'purchase_price': ingredient.purchase_price,
                'quantity': 0,
                'category': ingredient.category.id if ingredient.category else None,
                }
        js_data = json.dumps(ingredients)
        filter_form = modelform_factory(
            Ingredient,
            fields=('category',)
        )
        context = {'js_data': js_data, 'form': filter_form}
        return render(request, 'new_ingredient_incoming.html', context)


class IngredientInvoicesView(LoginRequiredMixin, generic.ListView):
    template_name = 'ingredient_invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return IngredientInvoice.objects.all()


class IngredientInvoiceView(LoginRequiredMixin, generic.DetailView):
    model = IngredientInvoice
    template_name = "ingredient_invoice.html"


class IngredientInvoiceCreate(LoginRequiredMixin, CreateView):
    model = IngredientInvoice
    fields = '__all__'
    success_url = reverse_lazy('ingredient_invoices')

    def get_context_data(self, **kwargs):
        context = super(IngredientInvoiceCreate, self).get_context_data(**kwargs)
        context['ingredient_invoices'] = IngredientInvoice.objects.all()
        return context


class IngredientInvoiceUpdate(LoginRequiredMixin, UpdateView):
    model = IngredientInvoice
    fields = '__all__'
    success_url = reverse_lazy('ingredient_invoices')
    template_name = 'ingredient_invoice_update.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientInvoiceUpdate, self).get_context_data(**kwargs)
        invoice = self.get_object()
        incomings = invoice.ingredientincoming_set.all()
        context['incomings'] = incomings
        sum = 0
        for incoming in incomings:
            sum += incoming.quantity * incoming.purchase_price
        context['sum'] = sum
        return context


class IngredientInvoiceDelete(LoginRequiredMixin, DeleteView):
    model = IngredientInvoice
    success_url = reverse_lazy('ingredient_invoices')


# Incomings views
class IngredientIncomingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'ingredient_incomings.html'
    context_object_name = 'incomings'

    def get_queryset(self):
        return IngredientIncoming.objects.all()


class IngredientIncomingView(LoginRequiredMixin, generic.DetailView):
    model = IngredientIncoming
    template_name = "ingredient_incoming.html"


class IngredientIncomingCreate(LoginRequiredMixin, CreateView):
    model = IngredientIncoming
    fields = '__all__'
    success_url = reverse_lazy('ingredient_incomings')


class IngredientIncomingUpdate(LoginRequiredMixin, UpdateView):
    model = IngredientIncoming
    fields = '__all__'
    success_url = reverse_lazy('ingredient_incomings')
    template_name = 'ingredient_incoming_update.html'


class IngredientIncomingDelete(LoginRequiredMixin, DeleteView):
    model = IngredientIncoming
    success_url = reverse_lazy('ingredient_incomings')


# Manufacturing views
class ManufacturingsView(LoginRequiredMixin, generic.ListView):
    template_name = 'manufacturings.html'
    context_object_name = 'manufacturings'

    def get_queryset(self):
        return Manufacturing.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ManufacturingsView, self).get_context_data(**kwargs)
        manufacturings = Manufacturing.objects.all()
        purchase_sum = 0
        sale_sum = 0
        for manufacturing in manufacturings:
            purchase_sum += manufacturing.product.purchase_price * manufacturing.quantity
            sale_sum += manufacturing.product.shop_price * manufacturing.quantity
        context['sale_sum'] = sale_sum
        context['purchase_sum'] = purchase_sum
        return context


class ManufacturingView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturing
    template_name = "manufacturing.html"


class ManufacturingCreate(LoginRequiredMixin, CreateView):
    model = Manufacturing
    form_class = ManufacturingForm
    # fields = '__all__'
    success_url = reverse_lazy('manufacturings')


class ManufacturingUpdate(LoginRequiredMixin, UpdateView):
    model = Manufacturing
    fields = '__all__'
    success_url = reverse_lazy('manufacturings')
    template_name = 'manufacturing_update.html'

    def get_context_data(self, **kwargs):
        context = super(ManufacturingUpdate, self).get_context_data(**kwargs)
        context['manufacturings'] = Manufacturing.objects.all()
        return context


class ManufacturingDelete(LoginRequiredMixin, DeleteView):
    model = Manufacturing
    success_url = reverse_lazy('manufacturings')
