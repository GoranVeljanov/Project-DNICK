"""homedecorshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homedecorapp.views import index, user_login, register, user_logout, create_category, category_page, \
    add_product_to_category, product_page, delete_product, delete_category, edit_category, checkout, order_success, \
    add_to_cart, cart, remove_from_cart,edit_product
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name="index"),
                  path('login/', user_login, name='user_login'),
                  path('logout/', user_logout, name='logout'),
                  path('register/', register, name='register'),
                  path('category/<int:category_id>/', category_page, name='category_page'),
                  path('create_category/', create_category, name='create_category'),
                  path('category/<int:category_id>/add_product/', add_product_to_category,
                       name='add_product_to_category'),
                  path('product/<int:product_id>/', product_page, name='product_page'),
                  path('product/<int:product_id>/edit/', edit_product, name='edit_product'),
                  path('delete_product/<int:product_id>/<int:category_id>/', delete_product, name='delete_product'),
                  path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
                  path('edit_category/<int:category_id>/', edit_category, name='edit_category'),
                  path('checkout/<int:product_id>/', checkout, name='checkout'),
                  path('order_success/', order_success, name='order_success'),
                  path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
                  path('cart/', cart, name='cart'),
                  path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
