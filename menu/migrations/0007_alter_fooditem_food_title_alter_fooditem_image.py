# Generated by Django 5.0.3 on 2024-06-11 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_fooditem_food_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(upload_to='foodimages'),
        ),
    ]
