# Generated by Django 4.1.1 on 2022-10-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_user_avatar_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='picture',
            field=models.ImageField(default='group.png', null=True, upload_to=''),
        ),
    ]
