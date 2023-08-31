# Generated by Django 3.2.20 on 2023-08-29 23:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homedecorapp', '0002_auto_20230829_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.CharField(default=0, help_text='Enter sizes separated by commas', max_length=200, verbose_name='Sizes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]