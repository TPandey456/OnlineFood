# Generated by Django 5.0.3 on 2024-06-14 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_alter_openinghours_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghours',
            options={'ordering': ('day', '-from_hour')},
        ),
    ]
