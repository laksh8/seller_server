from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_catalog, name='product_catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product_list/', views.product_list, name = 'product_list'),
]
