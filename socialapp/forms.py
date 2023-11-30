import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from .models import *
from django.utils.translation import gettext_lazy as _

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
years = reversed(range(this_year - 100, this_year + 1))


class LogInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', help_text='')
    password = forms.CharField(label='Пароль', help_text='', widget=forms.PasswordInput)


class SignUp(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='')
    password1 = forms.CharField(label='Пароль', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Подтверждение пароля', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'placeholder': 'name@mail.com'}))
    name = forms.CharField(label='Имя', help_text='')
    surname = forms.CharField(label='Фамилия', help_text='')
    secondname = forms.CharField(label='Отчество', help_text='', required=False)
    city = forms.ModelChoiceField(label='Город, страна', queryset=City.objects.all().order_by('name'), required=False)
    birthdate = forms.DateField(label='Дата рождения', required=False,
                                widget=SelectDateWidget(empty_label=('Год', 'Месяц', 'День'), months=months, years=years))
    bio = forms.Field(label='Информация о себе', widget=forms.Textarea, required=False)
    # avatar =
