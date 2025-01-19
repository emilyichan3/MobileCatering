from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    file = forms.FileField(required=False)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = User
        fields = ['username','file','email', 'password1', 'password2','dob']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['image','dob']        