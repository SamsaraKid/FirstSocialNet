# Generated by Django 4.2.5 on 2023-12-12 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_city_add_by_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
    ]