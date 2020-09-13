from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(
        max_length=200,
        unique=False)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return self.name

