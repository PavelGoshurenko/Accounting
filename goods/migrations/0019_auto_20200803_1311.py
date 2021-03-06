# Generated by Django 3.0.6 on 2020-08-03 13:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0018_auto_20200802_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 3), null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 3), null=True, verbose_name='Создана'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 3), null=True),
        ),
    ]
