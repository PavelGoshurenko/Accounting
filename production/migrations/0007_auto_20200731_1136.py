# Generated by Django 3.0.6 on 2020-07-31 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0006_auto_20200728_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinvoice',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date(2020, 7, 31), null=True, verbose_name='Создана'),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date(2020, 7, 31), null=True, verbose_name='Создана'),
        ),
    ]