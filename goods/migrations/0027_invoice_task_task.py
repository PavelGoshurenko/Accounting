# Generated by Django 3.0.6 on 2020-09-27 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0026_auto_20200911_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название задачи')),
                ('text', models.TextField(max_length=2000)),
                ('done', models.BooleanField(default=False)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_Task',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Task')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, to='goods.Invoice', verbose_name='Накладная')),
            ],
            bases=('goods.task',),
        ),
    ]
