from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 

from django.db.models import Q
from .models import Chat, Group
from .forms import GroupForm, SignupForm

# Create your views here.


# --------Login------------------------------------------

def loginPage(request):
    
    print('entra')
    page = 'login'
    

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('index')
    
    context = {'page':page}
    return render(request, 'Login_v1/login.html', context)

#---------------------------------------------------------

# --------Logout------------------------------------------

def logoutPage(request):
    logout(request)
    return redirect('login')

#---------------------------------------------------------

# --------Register------------------------------------------

def registerPage(request):
    form = SignupForm()
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration') 

    context = {
        'form':form,
    }
    return render(request, 'Login_v1/login.html', context)

#---------------------------------------------------------

# --------Index------------------------------------------

@login_required(login_url='login')
def index(request):
    
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    chats = Chat.objects.filter(
        Q(user_1 = request.user) &
        Q(user_2__username__icontains=q)
        )

    groups = Group.objects.filter(
        Q(users = request.user) &
        Q(name__icontains=q)
        )
    
    context =  {
        'groups':groups,
        'chats':chats,
        }

    return render(request, 'index.html', context)

#---------------------------------------------------------

# --------Room------------------------------------------

@login_required(login_url='login')
def room(request, pk):
    group = Group.objects.get(id=pk)
    chat_messages = group.message_set.all()
    
    if not request.user in group.users.all():
        messages.error(request,'No seas cotilla...')
        return redirect('index')
    
    if request.method == 'POST':
        group.users.remove(request.user)
        return redirect('index')


    context = {
        'group': group,
        'chat_messages': chat_messages
    }
    return render(request, 'chatroom.html', context)

#---------------------------------------------------------

# --------Contacts------------------------------------------

@login_required(login_url='login')
def contacts(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if request.method == 'POST':
        
        user_2_id = request.POST.get('contact')
        user_2 = User.objects.get(id=user_2_id)
        
        try:
            try:
                chat = Chat.objects.get(name=f'{request.user.id}_chat_{user_2_id}', user_2=user_2)
            except:
                chat = Chat.objects.get(name=f'{user_2_id}_chat_{request.user.id}', user_2=user_2)
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
    
    contacts = User.objects.filter(
        Q(username__icontains=q)
        )
    
    context = {
        'contacts':contacts,
    }

    return render(request, 'contacts.html', context)

#---------------------------------------------------------

# --------Chat------------------------------------------

@login_required(login_url='login')
def chat(request, chat_name):
    
    chat = Chat.objects.filter(name=chat_name)
    participants = (chat[0].user_1, chat[0].user_2)

    chat_messages = chat[0].messages.all()

    if not request.user in participants:
        
        messages.error(request,'No seas cotilla...')
        return redirect('index')
    
    
    context = {
        'chat_name' : chat_name,
        'chat_messages': chat_messages
        
    }
    return render(request, 'chat.html', context)

#---------------------------------------------------------

# --------Create Groups------------------------------------------

@login_required(login_url='login')
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
            form_instance.host = request.user
            form_instance.save()
            return redirect(f'chatroom/{form_instance.id}')

        
    users = User.objects.all()
    context = {
        'users': users,
        'form' : form
    }
    return render(request, 'group.html', context)

#---------------------------------------------------------

# --------Delete Chats------------------------------------------

def deleteChats(request, pk):
    object = Chat.objects.get(id=pk)
    
    if request.method == 'POST':
        object.delete()
        return redirect('index')

    context = {
        'object':object,
    }

    return render(request, 'deletePage.html', context)

#---------------------------------------------------------

# --------Delete Groups------------------------------------------

def deleteGroups(request, pk):
    object = Group.objects.get(id=pk)
    
    if request.method == 'POST':
        object.delete()
        return redirect('index')

    context = {
        'object':object,
    }

    return render(request, 'deletePage.html', context)

#---------------------------------------------------------
