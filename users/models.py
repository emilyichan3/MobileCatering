from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from PIL import Image # Change here from pillow import Image
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    dob = models.DateField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)