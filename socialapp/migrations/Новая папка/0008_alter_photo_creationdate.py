# Generated by Django 4.2.5 on 2024-01-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0007_alter_photo_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='creationdate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
