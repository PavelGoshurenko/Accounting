from django.contrib import admin
from money.models import Asset, Spending

# Register your models here.
admin.site.register(Spending)
admin.site.register(Asset)
