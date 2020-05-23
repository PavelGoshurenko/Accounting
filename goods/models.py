from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Наименование категории")

    def __str__(self):
        return self.name

    
class ProductBrand(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Бренд")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        help_text="Наименование товара")
    shop_price = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    purchase_price = models.FloatField(blank=False, null=False)
    internet_price = models.FloatField(blank=False, null=False)
    quantity = models.IntegerField(blank=False)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.ProtectedError,
        null=True,
        blank=True
        )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.ProtectedError,
        null=True,
        blank=True
        )

    def add_quantity(self, quantity, purchase_price):
        new_quantity = self.quantity + quantity
        new_purchase_price = (self.purchase_price * self.quantity + purchase_price * quantity) / new_quantity
        self.quantity = new_quantity
        self.purchase_price = new_purchase_price
        self.save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', args=[str(self.id)])

        
class Invoice(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Наименование накладной")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Incoming(models.Model):
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    invoice = models.ForeignKey(Invoice, on_delete=models.ProtectedError)
    purchase_price = models.FloatField(blank=False, null=False)
    quantity = models.IntegerField(blank=False)

