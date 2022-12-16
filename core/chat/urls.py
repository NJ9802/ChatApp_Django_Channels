from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('group_index', views.group_index, name='group-index'),
    path('chatroom/<int:pk>/', views.room, name='room'),
    path('contacts', views.contacts, name='contacts'),
    path('chat/conversation/<str:chat_name>', views.chat, name='chat'),
    path('new_group', views.create_group, name='group'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
    path('deleteChat/<int:pk>', views.deleteChats, name='deleteChat'),
    path('deleteGroup/<int:pk>', views.deleteGroups, name='deleteGroup'),
    path('profile', views.profile, name='profile'),
    path('notifications', views.notifications, name='notifications'),

]