from django.contrib import admin
from goods.models import Product, ProductCategory, ProductBrand, Invoice, Incoming

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Invoice)
admin.site.register(Incoming)
