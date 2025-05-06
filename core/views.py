from django.utils import timezone
from decimal import Decimal
from django.shortcuts import render

from core.utils.token_utils import decode_user_token
from .models import Order, OrderItem, Product

username = 'user'

def product_catalog(request):
    global username
    token = request.GET.get('token')

    cart = request.session.get('cart', {})
    cart_item_count = sum(cart.values())  # total quantity of all items

    user = decode_user_token(token)
    username = 'user'
    if user:
        username = user['username']   
    products = Product.objects.filter(available_quantity__gt=0)
    return render(request, 'catalog.html', {'products': products, 'username': username, 'cart_item_count': cart_item_count,})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('product_catalog')  # or wherever you want to redirect

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [
        {'product': p, 'quantity': cart[str(p.id)], 'total': p.price * cart[str(p.id)]}
        for p in products
    ]
    return render(request, 'cart.html', {'cart_items': cart_items})

def checkout(request):
    # Assuming the cart is stored in the session
    cart = request.session.get('cart', {})

    # Calculate the total amount
    total_amount = Decimal('0.00')
    items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_amount += product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price,
        })

    # Save the order to the database
    order = Order.objects.create(
        buyer = username,  # Assuming the user is logged in
        total_amount=total_amount,
        status='paid',  # You can change this based on payment gateway status
    )

    # Save the order items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
        )

    # Clear the cart after order is placed
    request.session['cart'] = {}

    # Send the order details to the success template
    return render(request, 'checkout_success.html', {
        'order_id': order.id,
        'estimated_delivery': timezone.now() + timezone.timedelta(days=7),  # Adjust this as needed
        'total_amount': total_amount,
        'name':username,
    })