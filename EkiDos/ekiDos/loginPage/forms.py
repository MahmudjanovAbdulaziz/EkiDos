from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class':'input100','placeholder':'Имя пользователя'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class':'input100','placeholder':'Mail аддрес'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Пароль'}))
    password2 = forms.CharField(label="Повторить Пароль", widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Повторить пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class':'input100',}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'input100'}))

    
