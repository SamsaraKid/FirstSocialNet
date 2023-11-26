from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LogInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', help_text='')
    password = forms.CharField(label='Пароль', help_text='', widget=forms.PasswordInput)


class SignUp(UserCreationForm):
    name = forms.CharField(label='Имя', help_text='')
    surname = forms.CharField(label='Фамилия', help_text='')
    username = forms.CharField(label='Имя пользователя', help_text='')
    password1 = forms.CharField(label='Пароль', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Подтверждение пароля', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'placeholder': 'name@mail.com'}))
