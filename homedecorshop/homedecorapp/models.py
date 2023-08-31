from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def get_products_by_price_range(self, min_price, max_price):
        products = Product.objects.filter(category=self, price__gte=min_price, price__lte=max_price)
        return products


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, default=' DECOR')
    color = models.CharField(max_length=200, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    size = models.CharField(max_length=255, default='One Size')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(default=timezone.now)
    material = models.CharField(max_length=255, default='')


class Order(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),

    ]
    product = models.ForeignKey(
        on_delete=models.CASCADE,
        to='homedecorapp.product',
        null=True,
    )
    shipping_address = models.TextField()
    name = models.TextField(max_length=50)
    surname = models.TextField(max_length=50)
    phone = models.TextField(max_length=9, default='')
    billing_address = models.TextField(default='')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
