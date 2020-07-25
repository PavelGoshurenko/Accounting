from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from production.models import Ingredient, IngredientIncoming, IngredientInvoice, Manufacturing
from django.views.generic.base import TemplateView
import openpyxl
from production.filters import IngredientFilter
import json
from django.forms import modelform_factory

# Ingredient views


class IngredientsView(generic.ListView):
    template_name = 'ingredients.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = IngredientFilter(
            self.request.GET,
            queryset=self.get_queryset(),
        )
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


class IngredientView(generic.DetailView):
    model = Ingredient
    template_name = "ingredient.html"


class IngredientCreate(CreateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('ingredients')

    def get_context_data(self, **kwargs):
        context = super(IngredientCreate, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context


class IngredientUpdate(UpdateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('ingredients')
    template_name = 'ingredient_update.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientUpdate, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context


class IngredientDelete(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredients')


class AddIngredientsView(TemplateView):

    template_name = "add_ingredients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wb = openpyxl.load_workbook('1.xlsx')
        sheet = wb.active
        i = 3
        while i < 2350:
            if sheet['A{}'.format(i)].value and sheet['I{}'.format(i)].value:
                new_ingredient = Ingredient(
                    name=sheet['A{}'.format(i)].value,
                    purchase_price=sheet['L{}'.format(i)].value,
                    quantity=sheet['G{}'.format(i)].value,
                    category=None,
                    )
                new_ingredient.save()
            i += 1
        return context


# invoices views

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


class IngredientInvoicesView(generic.ListView):
    template_name = 'ingredient_invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return IngredientInvoice.objects.all()


class IngredientInvoiceView(generic.DetailView):
    model = IngredientInvoice
    template_name = "ingredient_invoice.html"


class IngredientInvoiceCreate(CreateView):
    model = IngredientInvoice
    fields = '__all__'
    success_url = reverse_lazy('ingredient_invoices')

    def get_context_data(self, **kwargs):
        context = super(IngredientInvoiceCreate, self).get_context_data(**kwargs)
        context['ingredient_invoices'] = IngredientInvoice.objects.all()
        return context


class IngredientInvoiceUpdate(UpdateView):
    model = IngredientInvoice
    fields = '__all__'
    success_url = reverse_lazy('ingredient_invoices')
    template_name = 'ingredient_invoice_update.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientInvoiceUpdate, self).get_context_data(**kwargs)
        invoice = self.get_object()
        context['incomings'] = invoice.ingredientincoming_set.all()
        return context


class IngredientInvoiceDelete(DeleteView):
    model = IngredientInvoice
    success_url = reverse_lazy('ingredient_invoices')


# Incomings views
class IngredientIncomingsView(generic.ListView):
    template_name = 'ingredient_incomings.html'
    context_object_name = 'incomings'

    def get_queryset(self):
        return IngredientIncoming.objects.all()


class IngredientIncomingView(generic.DetailView):
    model = IngredientIncoming
    template_name = "ingredient_incoming.html"


class IngredientIncomingCreate(CreateView):
    model = IngredientIncoming
    fields = '__all__'
    success_url = reverse_lazy('ingredient_incomings')

    def get_context_data(self, **kwargs):
        context = super(IngredientIncomingCreate, self).get_context_data(**kwargs)
        context['incomings'] = IngredientIncoming.objects.all()
        return context


class IngredientIncomingUpdate(UpdateView):
    model = IngredientIncoming
    fields = '__all__'
    success_url = reverse_lazy('ingredient_incomings')
    template_name = 'ingredient_incoming_update.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientIncomingUpdate, self).get_context_data(**kwargs)
        context['incomings'] = IngredientIncoming.objects.all()
        return context


class IngredientIncomingDelete(DeleteView):
    model = IngredientIncoming
    success_url = reverse_lazy('ingredient_incomings')


# Manufacturing views
class ManufacturingsView(generic.ListView):
    template_name = 'manufacturings.html'
    context_object_name = 'manufacturings'

    def get_queryset(self):
        return Manufacturing.objects.all()


class ManufacturingView(generic.DetailView):
    model = Manufacturing
    template_name = "manufacturing.html"


class ManufacturingCreate(CreateView):
    model = Manufacturing
    fields = '__all__'
    success_url = reverse_lazy('manufacturings')

    def get_context_data(self, **kwargs):
        context = super(ManufacturingCreate, self).get_context_data(**kwargs)
        context['manufacturings'] = Manufacturing.objects.all()
        return context


class ManufacturingUpdate(UpdateView):
    model = Manufacturing
    fields = '__all__'
    success_url = reverse_lazy('manufacturings')
    template_name = 'manufacturing_update.html'

    def get_context_data(self, **kwargs):
        context = super(ManufacturingUpdate, self).get_context_data(**kwargs)
        context['manufacturings'] = Manufacturing.objects.all()
        return context


class ManufacturingDelete(DeleteView):
    model = Manufacturing
    success_url = reverse_lazy('manufacturings')
