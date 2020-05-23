# Assets views
class AssetsView(generic.ListView):
    template_name = 'Assets.html'
    context_object_name = 'Assets'

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
