from django.contrib import admin
from goods.models import Product, ProductCategory, ProductBrand, Invoice, Incoming, Sale, Inventory, Invoice_Task

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Invoice)
admin.site.register(Incoming)
admin.site.register(Sale)
admin.site.register(Inventory)
admin.site.register(Invoice_Task)
