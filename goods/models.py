from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from money.models import Department
from django.shortcuts import get_object_or_404


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

    class Meta:
        ordering = ['category', 'brand', 'created_at']

        
class Invoice(models.Model):
    name = models.CharField(
        max_length=200,
        unique=False,
        help_text="Наименование накладной")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Incoming(models.Model):
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    invoice = models.ForeignKey(Invoice, on_delete=models.ProtectedError)
    purchase_price = models.FloatField(blank=False, null=False)
    quantity = models.IntegerField(blank=False)

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение прихода
         автоматически меняло остатки'''
        if self.id:
            previous_incoming = Incoming.objects.get(id=self.id)
            previous_quantity = previous_incoming.quantity
        else:
            previous_quantity = 0
        related_product = self.product
        related_product.quantity = related_product.quantity + self.quantity - previous_quantity
        related_product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки к исходным значениям'''
        related_product = self.product
        related_product.quantity = related_product.quantity - self.quantity
        related_product.save()
        super().delete(*args, **kwargs)


class Sale(models.Model):
    date = models.DateField(null=True, blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.ProtectedError)
    price = models.FloatField(blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    quantity = models.IntegerField(blank=False)

    def save(self, *args, **kwargs):
        if self.id:
            previous_sale = Sale.objects.get(id=self.id)
            previous_quantity = previous_sale.quantity
        else:
            previous_quantity = 0
        related_product = self.product
        related_product.quantity = related_product.quantity - self.quantity + previous_quantity
        related_product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        related_product = self.product
        related_product.quantity = related_product.quantity + self.quantity
        related_product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return "{} s{}".format(self.department.name, self.date)
