from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from money.models import Department
from django.shortcuts import get_object_or_404
import datetime
from money.models import Asset
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Наименование категории")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    
class ProductBrand(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Бренд")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Наименование товара")
    shop_price = models.FloatField(blank=False, null=False, verbose_name="Цена магазин")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    purchase_price = models.FloatField(blank=False, null=False, verbose_name='Цена покупки')
    internet_price = models.FloatField(blank=False, null=False, verbose_name='Цена интернет')
    quantity = models.FloatField(
        blank=False,
        verbose_name='Количество',
        default=0
        )
    min_quantity = models.IntegerField(
        blank=True,
        verbose_name='Минимальное Количество',
        default=-1000
        )
    max_quantity = models.IntegerField(
        blank=True,
        verbose_name='Максимальное Количество',
        default=-1000
        )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.ProtectedError,
        null=True,
        blank=True,
        verbose_name='Категория'
        )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.ProtectedError,
        null=True,
        blank=True,
        verbose_name='Бренд'
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
        max_length=500,
        unique=True,
        verbose_name='Накладная')
    created_at = models.DateField(
        null=True,
        blank=True,
        default=timezone.now,
        verbose_name='Создана'
    )

    def cost(self):
        incomings = self.incoming_set.all()
        sum = 0
        for incoming in incomings:
            sum += incoming.quantity * incoming.purchase_price
        return sum

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
            previous_product = previous_incoming.product
            previous_product.quantity -= previous_quantity
            previous_product.save()
            previous_invoice_name = previous_incoming.invoice.name
            previous_asset = Asset.objects.get(name=previous_invoice_name)
            previous_asset.amount += previous_quantity * previous_incoming.purchase_price
            previous_asset.save()
        related_product = Product.objects.get(id=self.product.id)  # !!!
        related_product.quantity += self.quantity
        related_invoice_name = self.invoice.name
        try:
            asset_to_change = Asset.objects.get(name=related_invoice_name)
        except ObjectDoesNotExist:
            asset_to_change = Asset(name=related_invoice_name, amount=0)
        asset_to_change.amount -= self.quantity * self.purchase_price
        asset_to_change.save()
        related_product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки к исходным значениям'''
        related_product = self.product
        related_product.quantity = related_product.quantity - self.quantity
        related_product.save()
        asset_to_change = Asset.objects.get(name=self.invoice.name)
        asset_to_change.amount += self.quantity * self.purchase_price
        asset_to_change.save()
        super().delete(*args, **kwargs)


class Sale(models.Model):
    date = models.DateField(
        null=True,
        blank=True,
        default=timezone.now
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.ProtectedError)
    price = models.FloatField(blank=False, null=False)
    purchase_price = models.FloatField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    quantity = models.FloatField(blank=False)

    def cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.id:
            previous_sale = Sale.objects.get(id=self.id)
            previous_quantity = previous_sale.quantity
            previos_asset_name = '{} {}'.format(
                previous_sale.date,
                previous_sale.department.name)
            previous_asset = Asset.objects.get(name=previos_asset_name)
            previous_product = previous_sale.product
            previous_product.quantity += previous_quantity
            previous_product.save()
            previous_asset.amount -= previous_quantity * previous_sale.price
            previous_asset.save()
        related_product = Product.objects.get(id=self.product.id)
        related_product.quantity -= self.quantity
        related_product.save()
        asset_name = '{} {}'.format(self.date, self.department.name)
        try:
            asset_to_change = Asset.objects.get(name=asset_name)
        except ObjectDoesNotExist:
            asset_to_change = Asset(name=asset_name, amount=0)
        asset_to_change.amount += self.price * self.quantity
        asset_to_change.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        related_product = self.product
        related_product.quantity += self.quantity
        related_product.save()
        asset_name = '{} {}'.format(self.date, self.department.name)
        asset_to_change = Asset.objects.get(name=asset_name)
        asset_to_change.amount -= self.price * self.quantity
        asset_to_change.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return "{} s{}".format(self.department.name, self.date)


class Inventory(models.Model):
    date = models.DateField(
        null=True,
        blank=True,
        default=timezone.now
    )
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    supposed_quantity = models.FloatField(blank=False)
    fact_quantity = models.FloatField(blank=False, default=0)
    confirmed = models.BooleanField(blank=False, default=False)

    def shortage(self):
        return self.supposed_quantity - self.fact_quantity

    def cost(self):
        return self.shortage() * self.product.internet_price
    