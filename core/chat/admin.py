from django.contrib import admin
from .models import Chat, Group, Message, User, Notifications

# Register your models here.

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(Notifications)
