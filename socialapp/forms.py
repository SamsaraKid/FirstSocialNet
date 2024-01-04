import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm


months = {
    1: _("Январь"),
    2: _("Февраль"),
    3: _("Март"),
    4: _("Апрель"),
    5: _("Май"),
    6: _("Июнь"),
    7: _("Июль"),
    8: _("Август"),
    9: _("Сентябрь"),
    10: _("Октябрь"),
    11: _("Ноябрь"),
    12: _("Декабрь"),
}

this_year = datetime.date.today().year
years = range(this_year, this_year - 100, -1)


class LogInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', help_text='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class SignUp(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'Никнейм в адресной строке'}))
    password1 = forms.CharField(label='Пароль', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Подтверждение пароля', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'placeholder': 'name@mail.com'}))
    name = forms.CharField(label='Имя', help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    surname = forms.CharField(label='Фамилия', help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    secondname = forms.CharField(label='Отчество', help_text='', required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Отчество'}))
    birthdate = forms.DateField(label='Дата рождения',
                                widget=forms.SelectDateWidget(months=months,
                                                              years=years))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all().order_by('name'), required=False)
    country = forms.ModelChoiceField(label='Страна', queryset=Country.objects.all().order_by('name'), required=False)
    city_custom = forms.CharField(label='Город', max_length=50, required=False)
    bio = forms.CharField(label='Информация о вас', max_length=500, required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Максимум 500 знаков'}))
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


class PostForm(forms.Form):
    text = forms.CharField(label='Текст поста', max_length=500,
                          widget=forms.Textarea(attrs={'placeholder': 'Напишите что-нибудь. Максимум 500 знаков'}))
    # class Meta:
    #     model = Post
    #     fields = ('text',)