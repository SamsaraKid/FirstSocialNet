from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страна')


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')


class Language(models.Model):
    name = models.CharField(max_length=100, verbose_name='Язык')


class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name='Сообщество')
    description = models.TextField(verbose_name='Описание')
    creationdate = models.DateField(verbose_name='Сообщество')


class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    secondname = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='Город')
    languages = models.ManyToManyField(Language, verbose_name='Язык')
    birthdate = models.DateField(verbose_name='Дата рождения')
    communities = models.ManyToManyField(Community, verbose_name='Сообщества')


