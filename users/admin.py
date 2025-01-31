# from django.contrib import admin

# # Register your models here.
# from .models import Profile

# admin.site.register(Profile)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Profile

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Profile
    list_display = ("email", "is_staff", "is_active",'image','dob', 'isCaterer',)
    list_filter = ("email", "is_staff", "is_active",'image','dob', 'isCaterer',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("More",{"fields": ('image','dob', 'isCaterer')})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",'image','dob', 'isCaterer',
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Profile, CustomUserAdmin)