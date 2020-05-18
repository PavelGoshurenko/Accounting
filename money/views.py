from django.shortcuts import render, get_object_or_404
from money.models import Spending, Source
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views import generic


# Spending views
class SpendingsView(generic.ListView):
    template_name = 'spendings.html'
    context_object_name = 'spendings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sources'] = Source.objects.all()
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

    def form_valid(self, form):
        parameters = self.request.POST
        amount = parameters['amount']
        source_id = parameters['source']
        source = get_object_or_404(Source, id=source_id)
        source.amount = source.amount - float(amount)
        source.save()
        return super().form_valid(form)


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