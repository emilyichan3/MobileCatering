from django.db import models
from PIL import Image # Change here from pillow import Image
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Profile(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150,blank=True)
    last_name = models.CharField(_("last name"), max_length=150,blank=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    image = models.ImageField(default='user_default.jpg', upload_to='profile_pics')
    dob = models.DateField(default=datetime.utcnow)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
