from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatroom/<str:room_name>/', views.room, name='room'),
    path('contacts', views.contacts, name='contacts'),
    path('chat/conversation/<str:chat_name>', views.chat, name='chat'),
    path('new_group', views.create_group, name='group')
]