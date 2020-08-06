# Generated by Django 3.0.6 on 2020-08-02 11:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_auto_20200802_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.date(2020, 8, 2), null=True)),
                ('supposed_quantity', models.FloatField()),
                ('fact_quantity', models.FloatField(default=0)),
                ('confirmed', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='goods.Product')),
            ],
        ),
    ]