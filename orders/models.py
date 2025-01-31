from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Caterer(models.Model):
    caterer_name = models.CharField(max_length=60)
    caterer_description = models.TextField()
    location = models.CharField(max_length=200)
    activate = models.BooleanField(default=True)
    register = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caterer')
    
    def __str__(self):
        return f'{ self.caterer_name } is located at { self.location }'
    
class Menu(models.Model):
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    max_serve_qualities = models.IntegerField()
    available_from = models.DateTimeField(default=timezone.now)
    available_to = models.DateTimeField(default=timezone.now)
    sample_image = models.ImageField(default='menu_default.jpg', upload_to='menu_pics', blank=True, null=True)
    owner = models.ForeignKey(Caterer, on_delete=models.CASCADE, related_name='menu')

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
    

    
