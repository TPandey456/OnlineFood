# Generated by Django 5.0.3 on 2024-06-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_remove_vendor_modified_at_alter_vendor_user_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]
