# Generated by Django 5.0.3 on 2024-06-06 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='category_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditems', to='menu.category'),
        ),
    ]
