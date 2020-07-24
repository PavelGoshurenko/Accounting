from django.db import models
from django.urls import reverse
import datetime
from money.models import Asset
from goods.models import Product


class IngredientCategory(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Наименование категории")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name="Наименование ингредиента")
    purchase_price = models.FloatField(blank=False, null=False, verbose_name='Цена покупки')
    quantity = models.IntegerField(
        blank=False,
        verbose_name='Количество',
        default=0
        )
    category = models.ForeignKey(
        IngredientCategory,
        on_delete=models.ProtectedError,
        null=True,
        blank=True,
        verbose_name='Категория'
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
        return reverse('ingredients', args=[str(self.id)])

    class Meta:
        ordering = ['category']

        
class IngredientInvoice(models.Model):
    name = models.CharField(
        max_length=200,
        unique=False,
        verbose_name='Накладная')
    created_at = models.DateField(
        null=True,
        blank=True,
        default=datetime.date.today(),
        verbose_name='Создана'
    )
    paid = models.FloatField(
        verbose_name='Оплачено',
        blank=True,
        null=True,
        default=0)
    asset = models.ForeignKey(
        Asset,
        on_delete=models.ProtectedError,
        blank=True,
        null=True,
        verbose_name='Источник')

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение оплаты
         автоматически меняло остатки источника'''
        if self.id:
            previous_invoice = IngredientInvoice.objects.get(id=self.id)
            previous_paid = previous_invoice.paid
            previous_asset = previous_invoice.asset
            if previous_asset:
                previous_asset.amount += previous_paid
                previous_asset.save()
        if self.asset:
            related_asset = Asset.objects.get(id=self.asset.id)  # !!!
            related_asset.amount -= self.paid
            related_asset.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки актива к исходным значениям'''
        if self.asset:
            self.asset.amount += self.paid
            self.asset.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class IngredientIncoming(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.ProtectedError)
    invoice = models.ForeignKey(IngredientInvoice, on_delete=models.ProtectedError)
    purchase_price = models.FloatField(blank=False, null=False)
    quantity = models.IntegerField(blank=False)

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение прихода
         автоматически меняло остатки'''
        if self.id:
            previous_incoming = IngredientIncoming.objects.get(id=self.id)
            previous_quantity = previous_incoming.quantity
            previous_ingredient = previous_incoming.ingredient
            previous_ingredient.quantity -= previous_quantity
            previous_ingredient.save()
        related_ingredient = Ingredient.objects.get(id=self.ingredient.id)  # !!!
        related_ingredient.quantity += self.quantity
        related_ingredient.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки к исходным значениям'''
        related_ingredient = self.ingredient
        related_ingredient.quantity = related_ingredient.quantity - self.quantity
        related_ingredient.save()
        super().delete(*args, **kwargs)


class Proportion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.ProtectedError)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "В {} {} {}".format(self.product.name, self.quantity, self.ingredient.name)



