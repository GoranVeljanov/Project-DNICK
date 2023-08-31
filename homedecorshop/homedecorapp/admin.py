from django.contrib import admin
from django import forms
from .models import Category
from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem

admin.site.register(Category)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'shipping_address', 'order_date', 'payment_method')
    list_filter = ('order_date', 'payment_method')
    inlines = [OrderItemInline]
    actions = ['mark_as_pending', 'mark_as_sent', 'mark_as_delivered']

    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')

    def mark_as_sent(self, request, queryset):
        queryset.update(status='Sent')

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    mark_as_pending.short_description = "Select orders as Pending"
    mark_as_sent.short_description = "Select orders as Sent"
    mark_as_delivered.short_description = "Select orders as Delivered"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
