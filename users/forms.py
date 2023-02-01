from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label="Last Name", required=True)    
    is_staff = forms.BooleanField(label="Check if user is a manager", required=False, initial=False )
    class Meta:
        model = User
        fields = ['username', 'first_name',  'last_name', 'email', 'password1', 'password2', 'is_staff']
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'image']
