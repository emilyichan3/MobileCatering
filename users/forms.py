from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.validators import UnicodeUsernameValidator

User = get_user_model()
# xxx/admin/
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("email","first_name", "last_name",'image','dob')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ("email","first_name", "last_name",'image','dob')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = Profile
        fields = ['email', "first_name", "last_name", 'password1', 'password2', 'dob']


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ["first_name", "last_name",'image', 'dob']



