from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userauth.models import User

class UserRegisterForm(UserCreationForm):

    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ''}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))
    print(forms.CharField)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'firstname']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))
