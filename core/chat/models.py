from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length=50)
    
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    last_message = models.CharField(max_length = 100, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'Chat of {self.user_1} with {self.user_2}'

class Group(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='users')
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    chats = models.ManyToManyField(Chat, related_name='messages')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.body[:10]