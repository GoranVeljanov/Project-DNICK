# Generated by Django 3.2.20 on 2023-08-30 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homedecorapp', '0012_remove_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]