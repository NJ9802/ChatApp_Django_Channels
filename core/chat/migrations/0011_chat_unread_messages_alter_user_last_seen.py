# Generated by Django 4.1.4 on 2022-12-23 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_chat_wallpaper_alter_user_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='unread_messages',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 16, 42, 32, 117139)),
        ),
    ]