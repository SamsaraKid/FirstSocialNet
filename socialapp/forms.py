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
    city_custom_sign = forms.BooleanField(label='Признак нового города', required=False)
    bio = forms.CharField(label='Информация о вас', max_length=500, required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Максимум 500 знаков'}))
    avatar = forms.ImageField(label='Аватар', required=False)

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


class CommunityCreate(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('communityname', 'title', 'info', 'avatar', 'city')

    def clean_communityname(self):
        communityname = self.cleaned_data.get('communityname')
        if Community.objects.filter(slug=communityname) or Profile.objects.filter(slug=communityname):
            raise ValidationError('Выберите другое название для ссылки')
        else:
            return communityname

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Community.objects.filter(title=title):
            raise ValidationError('Выберите другое название')
        else:
            return title


class PostForm(forms.Form):
    text = forms.CharField(label='Текст поста', max_length=500,
                          widget=forms.Textarea(attrs={'placeholder': 'Напишите что-нибудь'}))
    photo = forms.ImageField(label='Фото', required=False)
    from_community = forms.BooleanField(label='От имени сообщества', required=False)

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('text', 'user',)
#         widgets = {'user': forms.HiddenInput,
#                    'text': forms.Textarea(attrs={'placeholder': 'Напишите что-нибудь'})}

class PeopleSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=500,
                          widget=forms.TextInput(attrs={'placeholder': 'Введите имя, фамилию или имя пользователя'}))

class CommunitySearchForm(forms.Form):
    query = forms.CharField(label='', max_length=500,
                          widget=forms.TextInput(attrs={'placeholder': 'Введите название группы'}))


class ProfileUpdate(forms.Form):
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
    city_custom_sign = forms.BooleanField(label='Признак нового города', required=False)
    bio = forms.CharField(label='Информация о вас', max_length=500, required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Максимум 500 знаков'}))
    avatar = forms.ImageField(label='Аватар', required=False)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar is None:
            return ''
        if 'image' not in avatar.content_type:
            raise forms.ValidationError('Неверный формат фото')
        return avatar


class CommunityUpdate(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('title', 'info', 'avatar', 'city')
    # title = forms.CharField(label='Название', help_text='',
    #                        widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    # city = forms.ModelChoiceField(label='Город', queryset=City.objects.all().order_by('name'), required=False)
    # info = forms.CharField(label='Информация о сообществе', max_length=500, required=False,
    #                       widget=forms.Textarea(attrs={'placeholder': 'Максимум 500 знаков'}))
    # avatar = forms.ImageField(label='Аватар', required=False)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar is None:
            return ''
        if 'image' not in avatar.content_type:
            raise forms.ValidationError('Неверный формат фото')
        return avatar

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if Community.objects.filter(title=title):
    #         raise ValidationError('Выберите другое название')
    #     else:
    #         return title


