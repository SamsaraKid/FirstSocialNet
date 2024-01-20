# Generated by Django 4.2.5 on 2024-01-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_alter_comment_creationdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='photo',
        ),
        migrations.AddField(
            model_name='comment',
            name='photo',
            field=models.ManyToManyField(to='socialapp.photo', verbose_name='Прикреплённые фото'),
        ),
    ]
