from django.contrib import admin
from production.models import IngredientInvoice, IngredientIncoming, Ingredient, IngredientCategory, Proportion

# Register your models here.
admin.site.register(IngredientInvoice)
admin.site.register(IngredientIncoming)
admin.site.register(Ingredient)
admin.site.register(IngredientCategory)
admin.site.register(Proportion)
