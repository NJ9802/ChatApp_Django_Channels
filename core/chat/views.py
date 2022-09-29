from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import Chat, Group
from .forms import GroupForm

# Create your views here.

def index(request):
    groups = Group.objects.filter(users = request.user)
    return render(request, 'index.html', {'groups':groups})

def room(request, room_name):
    return render(request, 'chatroom.html', {'room_name': room_name})

def contacts(request):
    if request.method == 'POST':
        
        user_2_id = request.POST['contact']
        user_2 = User.objects.get(id=user_2_id)
        try:
            chat = Chat.objects.get(name=f'{request.user.id}_chat_{user_2_id}', user_2=user_2)
            
        except:
            chat = Chat.objects.create(
            name = f'{request.user.id}_chat_{user_2_id}',
            user_1 = request.user,
            user_2 = user_2
            )
            
            chat_2 = Chat.objects.create(
                name = f'{request.user.id}_chat_{user_2_id}',
                user_1 = user_2,
                user_2 = request.user
            )
            
            chat.save()
            chat_2.save()
        return redirect(f'chat/conversation/{chat.name}')
    
    contacts = User.objects.all()
    
    context = {
        'contacts':contacts,
    }

    return render(request, 'contacts.html', context)

def chat(request, chat_name):
    
    context = {
        'chat_name' : chat_name,
    }
    return render(request, 'chat.html', context)

def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form_instance = form.save()
            users_id = request.POST.getlist('users')
            users_list = [User.objects.get(id=id)
                                for id in users_id]
            users_list.append(User.objects.get(username=request.user))
            form_instance.users.set(users_list)
            form_instance.save()
            return redirect(f'chatroom/room{form_instance.id}')

        
    users = User.objects.all()
    context = {
        'users': users,
        'form' : form
    }
    return render(request, 'group.html', context)