from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Menu, Order
import datetime

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
        

class OrderCreateForm(forms.ModelForm):
    product_name = forms.CharField(max_length=60)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = forms.DecimalField(max_digits=5, decimal_places=2)
    order_qualities = forms.IntegerField()
    pick_up_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    comment = forms.CharField(required=False, max_length=100)

    class Meta:
        model = Order
        fields = ['product_name', 
                'unit_price',
                'unit_discount_price',
                'order_qualities',
                'pick_up_at',
                'comment']
        
    def __init__(self, *args, **kwargs):
        menu = kwargs.pop('menu', None)  # Extract menu instance
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # Only set default for new forms, not existing ones
            self.fields['pick_up_at'].initial = datetime.date.today()

        if menu:
            self.fields['product_name'].initial = menu.product_name  
            self.fields['unit_price'].initial = menu.unit_price 
            self.fields['unit_discount_price'].initial = menu.unit_discount_price 
            
            # Make fields read-only if they shouldn't be changed
            self.fields['product_name'].widget.attrs['readonly'] = True
            self.fields['unit_price'].widget.attrs['readonly'] = True
            self.fields['unit_discount_price'].widget.attrs['readonly'] = True