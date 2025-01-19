from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Business(models.Model):
    business_name = models.CharField(max_length=60)
    business_description = models.TextField()
    location = models.CharField(max_length=200)
    activate = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{ self.business_name } is located at { self.location }'
    
class Menu(models.Model):
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    max_serve_qualities = models.IntegerField()
    sample_image = models.ImageField(upload_to='menu_pics', blank=True, null=True)
    owner = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='menu')

    def __str__(self):
        return f'{ self.product_name }'
    
class Order(models.Model):
    product_name = models.CharField(max_length=100)
    order_qualities = models.IntegerField()
    unit_discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')
    order_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order { self.id } is made by { self.customer.username}'
    

    
