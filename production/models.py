from django.db import models
from django.urls import reverse
import datetime
from money.models import Asset
from goods.models import Product
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


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
    quantity = models.FloatField(
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

    def save(self, *args, **kwargs):
        '''Изменение входной цены сохраняет разницу в актив'''
        if self.id:
            previous_ingredient = Ingredient.objects.get(id=self.id)
            previous_purchase_price = previous_ingredient.purchase_price
            if previous_purchase_price != self.purchase_price:
                asset = Asset.objects.get(name='Изменения цен')
                correction = self.purchase_price * self.quantity - previous_purchase_price * self.quantity
                asset.amount -= correction
                asset.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredients', args=[str(self.id)])

    class Meta:
        ordering = ['category']

        
class IngredientInvoice(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Накладная')
    created_at = models.DateField(
        null=True,
        blank=True,
        default=timezone.now,
        verbose_name='Создана'
    )

    def cost(self):
        incomings = self.ingredientincoming_set.all()
        sum = 0
        for incoming in incomings:
            sum += incoming.quantity * incoming.purchase_price
        return sum

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


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
            previous_invoice_name = previous_incoming.invoice.name
            previous_asset = Asset.objects.get(name=previous_invoice_name)
            previous_asset.amount += previous_quantity * previous_incoming.purchase_price
            previous_asset.save()
        related_ingredient = Ingredient.objects.get(id=self.ingredient.id)  # !!!
        related_ingredient.quantity += self.quantity
        related_invoice_name = self.invoice.name
        try:
            asset_to_change = Asset.objects.get(name=related_invoice_name)
        except ObjectDoesNotExist:
            asset_to_change = Asset(name=related_invoice_name, amount=0)
        asset_to_change.amount -= self.quantity * self.purchase_price
        asset_to_change.save()
        related_ingredient.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки к исходным значениям'''
        related_ingredient = self.ingredient
        related_ingredient.quantity = related_ingredient.quantity - self.quantity
        related_ingredient.save()
        asset_to_change = Asset.objects.get(name=self.invoice.name)
        asset_to_change.amount += self.quantity * self.purchase_price
        asset_to_change.save()
        super().delete(*args, **kwargs)


class Proportion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.ProtectedError)
    quantity = models.FloatField(blank=False)

    def __str__(self):
        return "В ({}) {} ({})".format(self.product.name, self.quantity, self.ingredient.name)


class Manufacturing (models.Model):
    product = models.ForeignKey(Product, on_delete=models.ProtectedError)
    quantity = models.IntegerField(blank=False)
    created_at = models.DateField(
        null=True,
        blank=True,
        default=timezone.now,
        verbose_name='Создана')

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение прихода
         автоматически меняло остатки'''
        if self.id:
            previous_manufacturing = Manufacturing.objects.get(id=self.id)
            previous_quantity = previous_manufacturing.quantity
            previous_product = previous_manufacturing.product
            previous_product.quantity -= previous_quantity
            asset_name = "Разлив {}".format(datetime.date.today().strftime('%B'))
            asset = Asset.objects.get(name=asset_name)
            product_cost = previous_product.purchase_price * previous_quantity
            previous_product.save()
            ingredients_cost = 0
            previous_proportions = Proportion.objects.filter(product=previous_product)
            for proportion in previous_proportions:
                ingredient = proportion.ingredient
                ingredient.quantity += previous_quantity * proportion.quantity
                ingredients_cost += previous_quantity * proportion.quantity * ingredient.purchase_price
                ingredient.save()
            asset.amount = asset.amount + product_cost - ingredients_cost
            asset.save()
        related_product = Product.objects.get(id=self.product.id)  # !!!
        asset_name = "Разлив {}".format(datetime.date.today().strftime('%B'))
        try:
            asset = Asset.objects.get(name=asset_name)
        except ObjectDoesNotExist:
            asset = Asset(
                name=asset_name,
                amount=0,
            )
        product_cost = related_product.purchase_price * self.quantity
        related_product.quantity += self.quantity
        related_product.save()
        ingredients_cost = 0
        relarted_proportions = Proportion.objects.filter(product=related_product)
        for proportion in relarted_proportions:
            ingredient = proportion.ingredient
            ingredient.quantity -= self.quantity * proportion.quantity
            ingredients_cost += self.quantity * proportion.quantity * ingredient.purchase_price
            ingredient.save()
        asset.amount = asset.amount - product_cost + ingredients_cost
        asset.save() 
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки к исходным значениям'''
        related_product = self.product
        asset_name = "Разлив {}".format(datetime.date.today().strftime('%B'))
        asset = Asset.objects.get(name=asset_name)
        product_cost = related_product.purchase_price * self.quantity
        related_product.quantity = related_product.quantity - self.quantity
        related_product.save()
        ingredients_cost = 0
        proportions = Proportion.objects.filter(product=self.product)
        for proportion in proportions:
            ingredient = proportion.ingredient
            ingredient.quantity += self.quantity * proportion.quantity
            ingredients_cost += self.quantity * proportion.quantity * ingredient.purchase_price
            ingredient.save()
        asset.amount = asset.amount + product_cost - ingredients_cost
        asset.save()
        super().delete(*args, **kwargs)
