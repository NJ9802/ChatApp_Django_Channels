# Generated by Django 4.1.1 on 2022-10-07 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_alter_chat_options_alter_group_options_chat_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.chat'),
        ),
    ]
