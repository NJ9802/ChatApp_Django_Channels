# Generated by Django 4.1.4 on 2022-12-23 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_user_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='wallpaper',
            field=models.ImageField(default='default-wallpaper.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 11, 14, 16, 195446)),
        ),
    ]
