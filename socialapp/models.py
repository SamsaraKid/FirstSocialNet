from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from django.utils.deconstruct import deconstructible

# @deconstructible
# class UploadToPath(object):
#     path = '{0}/{1}/{2}'
#
#     def __init__(self, sub_path):
#         self.sub_path = sub_path
#
#     def __call__(self, instance, filename):
#         return self.path.format(instance.user.username, self.sub_path, filename)

@deconstructible
class UploadToPath(object):
    path = '{0}/{1}/{2}'

    # def __init__(self, sub_path):
    #     self.sub_path = sub_path

    def __call__(self, instance, filename):
        return self.path.format(instance.user.username, instance.album, filename)



def avatar_upload_to(instance, filename):
    return os.path.join(os.path.join(instance.user.username, 'avatar'),
                        instance.user.username + os.path.splitext(filename)[1])

def community_avatar_upload_to(instance, filename):
    return os.path.join('communities', os.path.join(instance.communityname, 'avatar'),
                        instance.communityname + os.path.splitext(filename)[1])


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
    communityname = models.CharField(max_length=100, verbose_name='Название для ссылки')
    title = models.CharField(max_length=100, verbose_name='Название')
    info = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    avatar = models.ImageField(upload_to=community_avatar_upload_to, null=True, blank=True, verbose_name='Аватар')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    creationdate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    members = models.ManyToManyField(User, through='Membership', through_fields=('community', 'user'))
    slug = models.SlugField(unique=True, default=None, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.communityname)
        super(Community, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


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


@receiver(pre_delete, sender=Profile)
def avatar_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.avatar.delete(False)


class Photo(models.Model):
    # link = models.CharField(max_length=500, verbose_name='Адрес фото')
    album = models.CharField(max_length=500, verbose_name='Альбом фото')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    link = models.ImageField(upload_to=UploadToPath())
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Размещено в сообществе')
    creationdate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    like = models.ManyToManyField(User, verbose_name='Пользователи, поставившие лайк', related_name='photolikers')

    def count_likes(self):
        return len(self.like.all())



@receiver(pre_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.link.delete(False)


class Post(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст записи')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Размещено в сообществе')
    photo = models.ManyToManyField(Photo, verbose_name='Прикреплённые фото')
    creationdate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    like = models.ManyToManyField(User, verbose_name='Пользователи, поставившие лайк', related_name='postlikers')
    from_community = models.BooleanField(verbose_name='Пост от имени сообщества', null=True, blank=True)

    def count_comments(self):
        return len(self.comment_set.values())

    def count_likes(self):
        return len(self.like.all())


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост комментария')
    photo = models.ManyToManyField(Photo, verbose_name='Прикреплённые фото')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    creationdate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    like = models.ManyToManyField(User, verbose_name='Пользователи, поставившие лайк', related_name='commentlikers')
    from_community = models.BooleanField(verbose_name='Комментарий от имени сообщества', null=True, blank=True)

    def count_likes(self):
        return len(self.like.all())


