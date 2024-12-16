from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItems, Order, OrderItem
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,login
from django.db import transaction
from django.contrib import messages

# Create your views here.
#view for Homepage
def home_page(request):
    return render(request, "cart/home_page.html")

#view for creating an account for user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('cart:login')  # Redirect to login page
        else:
            messages.error(request, "There was an error creating your account. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'cart/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to 'next' if provided, else redirect to homepage
            next_url = request.GET.get('next', 'cart:home_page')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'cart/login.html')
#List of products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/product_list.html', 
                  {
                      "products" : products
                  })

#Selecting products to a cart
@login_required
def add_products_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_item, created=CartItems.objects.get_or_create(cart = cart, product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    #print(redirect("cart:view_cart"))
    return redirect("cart:view_cart")

#displaying the items in the cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_items = cart.items.all()
    total = sum( items.product.price* items.quantity for items in cart_items)
    return render(request, "cart/view_cart.html", {
        "cart_items":cart_items,
        "total": total
    })

#view for creating an order
@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('cart:view_cart')  # Redirect if cart is empty

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

        # Update product stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clear the cart
    cart.items.all().delete()

    return redirect('cart:order_successfull', order_id=order.id)

#view after the order is placed successfully
@login_required
def order_successfull(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'cart/order_successfull.html', {'order': order})