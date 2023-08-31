from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

    image = forms.ImageField(label='Category Image', required=False)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'color', 'price', 'description', 'size', 'image', 'material']


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    shipping_address = forms.CharField(max_length=100)
    billing_address = forms.CharField(max_length=100)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
