from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.validators import UnicodeUsernameValidator

User = get_user_model()
# xxx/admin/
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = Profile
        fields = ("email",'image','dob', 'isCaterer')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ("email",'image','dob', 'isCaterer')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    isCaterer = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = Profile
        fields = ['email', 'username', 'password1', 'password2', 'dob', 'isCaterer']


# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = Profile
#         fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[UnicodeUsernameValidator()],
        help_text="150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    isCaterer = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Profile
        fields = ['username','image','dob', 'isCaterer']



