# Generated by Django 3.0.6 on 2020-08-02 06:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_auto_20200801_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 2), null=True, verbose_name='Создана'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 2), null=True),
        ),
    ]
