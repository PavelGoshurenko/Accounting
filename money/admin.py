from django.contrib import admin
from money.models import Asset, Spending, Department, Transfer, SpendingCategory, Period, Constants

# Register your models here.
admin.site.register(Spending)
admin.site.register(Asset)
admin.site.register(Department)
admin.site.register(Transfer)
admin.site.register(SpendingCategory)
admin.site.register(Period)
admin.site.register(Constants)
