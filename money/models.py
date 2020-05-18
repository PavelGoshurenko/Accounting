from django.db import models
from django.urls import reverse


class Source(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Хранилище денег")
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
    source = models.ForeignKey(Source, on_delete=models.ProtectedError)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spending', args=[str(self.id)])
