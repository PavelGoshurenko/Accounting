# Generated by Django 3.0.6 on 2020-07-24 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_auto_20200721_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date(2020, 7, 24), null=True, verbose_name='Создана'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 7, 24), null=True),
        ),
    ]
