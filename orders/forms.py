from django import forms
from django.contrib.auth import get_user_model
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from .models import Menu, Order
from datetime import date
from django.core.exceptions import ValidationError

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

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")
        if available_from and available_to:
            if available_to < available_from:
                raise ValidationError("The due available date must be greater than the available from date.")

        if available_to:
            if available_to < date.today():
                raise ValidationError("The due available date cannot be in the past.")
    
        return cleaned_data
        
    
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
            self.fields['pick_up_at'].initial = date.today()

        if menu:
            self.fields['product_name'].initial = menu.product_name  
            self.fields['unit_price'].initial = menu.unit_price 
            self.fields['unit_discount_price'].initial = menu.unit_discount_price 
            
            # Make fields read-only if they shouldn't be changed
            self.fields['product_name'].widget.attrs['readonly'] = True
            self.fields['unit_price'].widget.attrs['readonly'] = True
            self.fields['unit_discount_price'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        pick_up_at = cleaned_data.get("pick_up_at")

        if pick_up_at and pick_up_at < date.today():
            raise ValidationError("The pick-up date cannot be in the past.")
        return cleaned_data