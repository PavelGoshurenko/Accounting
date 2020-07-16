from django.db import models
from django.urls import reverse
from datetime import datetime, date


class Asset(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Актив")
    amount = models.FloatField(
        verbose_name='Сумма',
        null=False, blank=False
        )

    def __str__(self):
        return self.name


class Spending(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Трата")
    amount = models.FloatField(
        verbose_name="Сумма",
        null=False, blank=False
        )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.ProtectedError,
        verbose_name='Источник')
    created_at = models.DateTimeField(
        default=datetime.now,
        null=True,
        verbose_name='Дата')

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение расхода
         автоматически меняло остатки источника'''
        if self.id:
            previous_spending = Spending.objects.get(id=self.id)
            previous_amount = previous_spending.amount
            previous_asset = previous_spending.asset
            previous_asset.amount += previous_amount
            previous_asset.save()
            if previous_asset == self.asset:
                previous_asset.amount -= self.amount
                previous_asset.save()
                super().save(*args, **kwargs)
                return
        self.asset.amount -= self.amount
        self.asset.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки актива к исходным значениям'''
        self.asset.amount += self.amount
        self.asset.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('asset', args=[str(self.id)])


class Transfer(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Перевод")
    amount = models.FloatField(
        help_text="Сумма",
        null=False, blank=False
        )
    asset_from = models.ForeignKey(
        Asset, on_delete=models.ProtectedError,
        related_name='asset_from'
        )
    asset_to = models.ForeignKey(
        Asset,
        on_delete=models.ProtectedError,
        related_name='asset_to')

    def save(self, *args, **kwargs):
        if self.id:
            previous_transfer = Transfer.objects.get(id=self.id)
            previous_amount = previous_transfer.amount
            previous_asset_from = previous_transfer.asset_from
            previous_asset_to = previous_transfer.asset_to
            previous_asset_from.amount += previous_amount
            previous_asset_to.amount -= previous_amount
            previous_asset_from.save()
            previous_asset_to.save()
        # Берем значения активов с БД т.к. они после сохранения не совпадают с self.assets
        related_asset_from = Asset.objects.get(id=self.asset_from.id)
        related_asset_to = Asset.objects.get(id=self.asset_to.id)
        related_asset_from.amount -= self.amount
        related_asset_to.amount += self.amount
        related_asset_from.save()
        related_asset_to.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        related_asset_from = self.asset_from
        related_asset_to = self.asset_to
        related_asset_from.amount += self.amount
        related_asset_to.amount -= self.amount
        related_asset_from.save()
        related_asset_to.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('transfer', args=[str(self.id)])
  

class Department(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Наименование отдела")

    def __str__(self):
        return self.name
