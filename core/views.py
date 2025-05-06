from django.shortcuts import render

from core.utils.token_utils import decode_user_token
from .models import Product

def product_catalog(request):
    token = request.GET.get('token')
    user = decode_user_token(token)
    username = 'user'
    if user:
        username = user['username']   
    products = Product.objects.filter(available_quantity__gt=0)
    return render(request, 'catalog.html', {'products': products, 'username': username})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

