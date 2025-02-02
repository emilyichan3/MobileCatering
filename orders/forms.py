from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Menu

User = get_user_model()

class MenuCreateForm(forms.ModelForm):
    product_name = forms.CharField(max_length=150)
    product_description = forms.CharField(max_length=150)
    available_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    available_to = forms.DateField( widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Menu
        fields = ['product_name', 
                'product_description',
                'unit_price',
                'unit_discount_price',
                'max_serve_qualities',
                'available_from',
                'available_to',
                'sample_image']