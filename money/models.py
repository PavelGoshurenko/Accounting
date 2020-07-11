from django.db import models
from django.urls import reverse


class Asset(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Актив")
    amount = models.FloatField(
        help_text="Колличество денег",
        null=False, blank=False
        )

    def __str__(self):
        return self.name


class Spending(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Трата")
    amount = models.FloatField(
        help_text="Колличество потраченных денег",
        null=False, blank=False
        )
    asset = models.ForeignKey(Asset, on_delete=models.ProtectedError)

    def save(self, *args, **kwargs):
        '''Переопределям save() чтобы появление / изменение расхода
         автоматически меняло остатки источника'''
        if self.id:
            previous_spending = Spending.objects.get(id=self.id)
            previous_amount = previous_spending.amount
        else:
            previous_amount = 0
        related_asset = self.asset
        related_asset.amount = related_asset.amount - self.amount + previous_amount
        related_asset.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''Переопределяем delete для того чтобы вернуть остатки актива к исходным значениям'''
        related_asset = self.asset
        related_asset.amount = related_asset.amount + self.amount
        related_asset.save()
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
        else:
            previous_amount = 0
        related_asset_from = self.asset_from
        related_asset_to = self.asset_to
        related_asset_from.amount = related_asset_from.amount - self.amount + previous_amount
        related_asset_to.amount = related_asset_to.amount + self.amount - previous_amount
        related_asset_from.save()
        related_asset_to.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        related_asset_from = self.asset_from
        related_asset_to = self.asset_to
        related_asset_from.amount = related_asset_from.amount + self.amount
        related_asset_to.amount = related_asset_to.amount - self.amount
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
