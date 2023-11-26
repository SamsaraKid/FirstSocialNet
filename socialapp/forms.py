from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LogInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', help_text='')
    password = forms.CharField(label='Пароль', help_text='', widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {'password': forms.PasswordInput()}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname']