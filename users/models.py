from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from PIL import Image # Change here from pillow import Image
from datetime import datetime

from django.contrib.auth.models import AbstractUser

# User = get_user_model()

# class User(AbstractUser):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     mobile_number = models.CharField(max_length=13, null=False, unique=True)
#     USERNAME_FIELD = "user"

#     REQUIRED_FIELDS = ["username"]

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='user_default.jpg', upload_to='profile_pics')
#     dob = models.DateField(default=datetime.utcnow)
#     isCaterer = models.BooleanField(default=False)
    
#     def __str__(self):
#         return f'{self.user.username} Profile'
    

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         with Image.open(self.image.path) as img:
#             if img.height > 300 or img.width > 300:
#                 output_size = (300, 300)
#                 img.thumbnail(output_size)
#                 img.save(self.image.path)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class Profile(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],  # Correctly applying UnicodeUsernameValidator
    )
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    image = models.ImageField(default='user_default.jpg', upload_to='profile_pics')
    dob = models.DateField(default=datetime.utcnow)
    isCaterer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
