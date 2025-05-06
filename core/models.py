from django.db import models
from django.contrib.auth.models import User

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # or Seller model
    available_quantity = models.IntegerField()

class Order(models.Model):
    buyer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')])

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='invoices')

class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    shipping_status = models.CharField(max_length=20)
