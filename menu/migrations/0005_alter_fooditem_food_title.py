# Generated by Django 5.0.3 on 2024-06-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_title',
            field=models.CharField(max_length=100),
        ),
    ]
