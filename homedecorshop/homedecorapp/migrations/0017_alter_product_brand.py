# Generated by Django 3.2.20 on 2023-08-31 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homedecorapp', '0016_auto_20230830_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(default=' DECOR', max_length=200),
        ),
    ]
