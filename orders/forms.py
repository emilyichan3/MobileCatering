from django import forms
from django.contrib.auth import get_user_model
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from .models import Menu, Order
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class MenuCreateForm(forms.ModelForm):
    product_name = forms.CharField(max_length=150)
    product_description = forms.CharField(max_length=150)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = forms.DecimalField(max_digits=5, decimal_places=2)   
    available_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    available_to = forms.DateField( widget=forms.DateInput(attrs={'type': 'date'}))
    sample_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'clearable': 'false'}))

    class Meta:
        model = Menu
        fields = ['product_name', 
                'product_description',
                'unit_price',
                'unit_discount_price',
                'available_from',
                'available_to',
                'sample_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  
            # Only set default for new forms, not existing ones
            self.fields['available_from'].initial = date.today()
            # Default available_to is 14 days
            self.fields['available_to'].initial = date.today() + timedelta(days=14)  

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")
        unit_price = cleaned_data.get("unit_price")
        unit_discount_price = cleaned_data.get("unit_discount_price")
        if available_from and available_to:
            if available_to < available_from:
                raise ValidationError("The due available date must be later than the available from date.")

        if available_to:
            if available_to < date.today():
                raise ValidationError("The due available date must be today or a future date.")

        if unit_price is not None and unit_discount_price is not None:
            if unit_price < unit_discount_price:
                raise ValidationError("The unit price cannot exceed the pre-order unit price.")
        
        return cleaned_data
        
    
class OrderCreateForm(forms.ModelForm):
    product_name = forms.CharField(max_length=60)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    unit_discount_price = forms.DecimalField(max_digits=5, decimal_places=2)
    order_qualities = forms.IntegerField(
                label="Order quantity (maximum is 200)",  # Ensure this line is included
                validators=[MinValueValidator(1), MaxValueValidator(200)])
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
            raise ValidationError("Please select a pick-up date that is today or in the future.")
        return cleaned_data
    
    