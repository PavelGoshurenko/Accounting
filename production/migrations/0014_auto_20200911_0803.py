# Generated by Django 3.0.6 on 2020-09-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0013_auto_20200806_0606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientinvoice',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='ingredientinvoice',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='ingredientinvoice',
            name='paid',
        ),
        migrations.AlterField(
            model_name='ingredientinvoice',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Накладная'),
        ),
    ]
