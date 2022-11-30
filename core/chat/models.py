from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    
    bio = models.TextField(default="Hey, i'm using Chat App")
    avatar = models.ImageField(default='avatar.png')
    unread_notifications = models.IntegerField(default=0)

    class Meta:
        ordering = ['username']


class Chat(models.Model):
    name = models.CharField(max_length=50)
    
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    last_message = models.CharField(max_length = 100, null=True)
    last_message_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'Chat of {self.user_1} with {self.user_2}'

class Group(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='users')
    last_message = models.CharField(max_length = 100, null=True)
    last_message_time = models.DateTimeField(null=True)
    picture = models.ImageField(default='group.png', null=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    chats = models.ManyToManyField(Chat, related_name='messages',)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.body[:30]

class Notifications(models.Model):
    body = models.CharField(max_length=50)
    from_to = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinatary')
    link = models.CharField(max_length=50)

    def __str__(self):
        return f'Notification from {self.from_to} to {self.to}'