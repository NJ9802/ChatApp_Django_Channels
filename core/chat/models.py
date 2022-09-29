from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length=50)
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Chat of {self.user_1} with {self.user_2}'

class Group(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='users')
    
    def __str__(self):
        return self.name