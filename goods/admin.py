from django.contrib import admin
from goods.models import Product, ProductCategory, ProductBrand, Invoice, Incoming, Sale, Inventory, Task


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'shortage', 'confirmed')
    list_filter = ('confirmed', )


# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Invoice)
admin.site.register(Incoming)
admin.site.register(Sale)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Task)
