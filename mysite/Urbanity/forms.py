from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Urbanity.models import Customer

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    phonenumber = forms.CharField(max_length=16, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    class Meta:
        model = User
        fields=['username','email', 'phonenumber','password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

class UserLoginForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    class Meta:
        model = User
        fields=['username','password1']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

class OTPForm(forms.ModelForm):
    otp = forms.TextInput(attrs={'placeholder': 'Enter OTP', 'class': 'textinputclass'})

    class Meta:
        model = Customer
        fields=['otp']
