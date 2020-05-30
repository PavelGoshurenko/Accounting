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
