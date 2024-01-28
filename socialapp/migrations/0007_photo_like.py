# Generated by Django 4.2.5 on 2024-01-20 14:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialapp', '0006_comment_like_alter_post_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='like',
            field=models.ManyToManyField(related_name='photolikers', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи, поставившие лайк'),
        ),
    ]