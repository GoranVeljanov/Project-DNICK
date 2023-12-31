# Generated by Django 3.2.20 on 2023-08-29 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homedecorapp', '0004_auto_20230829_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homedecorapp.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(),
        ),
    ]
