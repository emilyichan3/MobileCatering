from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

User = get_user_model()

class Caterer(models.Model):
    caterer_name = models.CharField(max_length=60)
    caterer_description = models.CharField(max_length=200)
    location = models.CharField(max_length=120)
    activate = models.BooleanField(default=True)
    register = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caterer')
    
    def __str__(self):
        return f'{ self.caterer_name } is located at { self.location }'
    
    def get_absolute_url(self):
        return reverse('orders-mycaterer', kwargs={'user_id': self.register.id})


class Menu(models.Model):
    product_name = models.CharField(max_length=60)
    product_description = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    available_from = models.DateField(default=timezone.now)
    available_to = models.DateField(default=timezone.now)
    # below code is for storing images locally.
    # sample_image = models.ImageField(default='menu_default.jpg', upload_to='menu_pics', blank=True, null=True)
    sample_image = models.ImageField(upload_to='menu_pics', storage=MediaCloudinaryStorage(), null=True, blank=True)
    caterer = models.ForeignKey(Caterer, on_delete=models.CASCADE, related_name='menu')
    register = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu')

    def __str__(self):
        return f'{ self.product_name }'
    
    def get_image_url(self):
        if self.sample_image: # Generate a Cloudinary thumbnail URL
            return cloudinary_url(
                self.sample_image.name, width=400, height=400, crop="lfill"
            )[0]
        else: # Fallback to static default image
            return static('orders/menu_default.png')
        
class Order(models.Model):
    product_name = models.CharField(max_length=60)
    order_qualities = models.IntegerField()
    unit_discount_price = models.DecimalField(max_digits=5, decimal_places=2)
    pick_up_at = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=100)
    status = models.CharField(max_length=60)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')
    order_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order { self.id } is made by { self.customer.username}'
    

    
