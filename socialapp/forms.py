from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LogInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', help_text='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', help_text='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class SignUp(UserCreationForm):
    name = forms.CharField(label='Имя', help_text='')
    surname = forms.CharField(label='Фамилия', help_text='')
    username = forms.CharField(label='Имя пользователя', help_text='')
    password1 = forms.CharField(label='Пароль', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Подтверждение пароля', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'placeholder': 'name@mail.com'}))
    avatar = forms.ImageField(label='Аватар')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar is None:
            raise forms.ValidationError('Добавьте фото')
        if 'image' not in avatar.content_type:
            raise forms.ValidationError('Неверный формат фото')
        return avatar

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('Такой пользователь уже существует')
        except User.DoesNotExist:
            return username
