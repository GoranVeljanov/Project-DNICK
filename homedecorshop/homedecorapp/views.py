from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CategoryForm, ProductForm, CheckoutForm
from .models import Category, Product, Order, Cart, CartItem
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages


def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def is_administrator(user):
    return user.is_staff


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_login')
        else:
            error_message = "Invalid registration information. Please check the form."
            return render(request, 'error.html', {'error_message': error_message})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid username or password."
            return render(request, 'error.html', {'error_message': error_message})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('index')


def category_page(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    price_sort = request.GET.get('price_sort')
    all_categories = Category.objects.all()

    if price_sort == 'min':
        products = products.order_by('price')
    elif price_sort == 'max':
        products = products.order_by('-price')

    context = {
        'category': category,
        'products': products,
        'all_categories': all_categories,
    }
    return render(request, 'categoryPage.html', context)


@user_passes_test(is_administrator)
def create_category(request, category_id=None):
    category = None

    if category_id:
        category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'createCategory.html', {'form': form})


def add_product_to_category(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            return redirect('category_page', category_id=category.id)
    else:
        form = ProductForm()

    return render(request, 'createProduct.html', {'category': category, 'form': form})


def product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    active_category = product.category

    related_products = Product.objects.filter(category=active_category).exclude(id=product_id)[:3]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'productPage.html', context)


def delete_product(request, product_id, category_id):
    product = get_object_or_404(Product, id=product_id)
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        product.delete()
        return redirect('category_page', category_id=category_id)

    return render(request, 'delete_product.html', {'product': product})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_page', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'createProduct.html', {'form': form, 'product': product})


@user_passes_test(is_administrator)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page or another appropriate page
    else:
        form = CategoryForm(instance=category)

    return render(request, 'createCategory.html', {'form': form, 'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('index')  # Redirect to the index page or another appropriate page

    return render(request, 'delete_category.html', {'category': category})


def order_success(request):
    return render(request, 'orderSuccess.html')


def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the payment using the selected payment method (e.g., dummy logic)

            # Create an order record in the database
            shipping_address = form.cleaned_data['shipping_address']
            billing_address = form.cleaned_data['billing_address']
            payment_method = form.cleaned_data['payment_method']

            order = Order.objects.create(
                product=product,
                shipping_address=shipping_address,
                billing_address=billing_address,
                payment_method=payment_method
            )

            return redirect('order_success')  # Redirect to order success page
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'product': product})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_page', product_id=product_id)


def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    cart_items = []
    total_price = 0

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.price * cart_item.quantity
            total_price += cart_item.total_price

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.delete()
    return redirect('cart')
