from django.contrib import admin

# Register your models here.
from .models import Order, Menu, Caterer

admin.site.register(Order)
admin.site.register(Menu)
admin.site.register(Caterer)