# Generated by Django 3.0.6 on 2020-08-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0013_auto_20200812_0514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spending',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Трата'),
        ),
    ]
