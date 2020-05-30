from django.contrib import admin
from money.models import Asset, Spending, Department, Transfer

# Register your models here.
admin.site.register(Spending)
admin.site.register(Asset)
admin.site.register(Department)
admin.site.register(Transfer)
