# Generated by Django 3.0.6 on 2020-08-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0022_auto_20200806_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='paid',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Накладная'),
        ),
    ]
