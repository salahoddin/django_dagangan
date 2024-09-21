from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # logged in users or anonymous users

    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=300)
    address_2 = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, null=True, blank=True) # becomes optional field
    postal_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'shipping address'

    def __str__(self):
        return f"Shitping address - {self.id}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #fk
    
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    ammount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Order - #{self.id}' # order object .id
    

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #fk
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Order Item - #{self.id}' # order object .id
