from django.contrib import admin
from .models import Invoice, Order, OrderItem, Product, SellerProfile
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Order
from .utils.invoice_utils import generate_invoice

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'created_at', 'status', 'total_amount', 'invoice_link']
    actions = ['download_invoice']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('invoice/<int:order_id>/', self.admin_site.admin_view(self.invoice_view), name='order-invoice'),
        ]
        return custom_urls + urls

    def invoice_view(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        return generate_invoice(order)

    def invoice_link(self, obj):
        return format_html('<a href="{}">Download</a>', f'/admin/core/order/invoice/{obj.id}/')
    invoice_link.short_description = 'Invoice'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller', 'available_quantity')
    search_fields = ('name',)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'custom_css']


admin.site.register(OrderItem)