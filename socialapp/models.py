from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


def avatar_upload_to(instance, filename):
    return os.path.join(os.path.join(instance.user.username, 'avatar'), instance.user.username + os.path.splitext(filename)[1])


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страна')

    def __str__(self):
        return f'{self.name}'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    add_by_user = models.BooleanField(verbose_name='Добавлен пользователем', default=False)

    def __str__(self):
        return f'{self.name}, {self.country.name}'


class Community(models.Model):
    communityname = models.CharField(max_length=100, verbose_name='Название для ссылки в адресной строке [A-Za-z0-9]')
    title = models.CharField(max_length=100, verbose_name='Название')
    info = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    avatar = models.CharField(max_length=500, null=True, blank=True, verbose_name='Аватар')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    creationdate = models.DateField(verbose_name='Дата создания')
    members = models.ManyToManyField(User, through='Membership', through_fields=('community', 'user'))
    slug = models.SlugField(unique=True, default=None, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.communityname)
        super(Community, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('community_detail', kwargs={'slug': self.slug})


class Membership(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(verbose_name='Роль участника в сообществе (0 - участник, 1 - администратор)')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    secondname = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    birthdate = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True, verbose_name='Аватар')
    # avatar = models.CharField(max_length=500, null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name='Информация')
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True, verbose_name='Подписки')
    slug = models.SlugField(unique=True, default=None, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Photo(models.Model):
    link = models.CharField(max_length=500, verbose_name='Адрес фото')
    album = models.CharField(max_length=500, verbose_name='Альбом фото')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Размещено в сообществе')
    creationdate = models.DateTimeField(verbose_name='Дата создания')


class Post(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст записи')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Размещено в сообществе')
    photo = models.ManyToManyField(Photo, verbose_name='Прикреплённые фото')
    creationdate = models.DateTimeField(verbose_name='Дата создания')


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост комментария')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Фото комментария')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    creationdate = models.DateTimeField(verbose_name='Дата создания')


