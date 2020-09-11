# Generated by Django 3.0.6 on 2020-09-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0025_sale_period'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
