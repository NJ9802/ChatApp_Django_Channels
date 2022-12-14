from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import Chat, Group, Notifications
from .forms import GroupForm, SignupForm

# Create your views here.


# --------Login------------------------------------------

def loginPage(request):

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

    context = {'page': page}
    return render(request, 'Login_v1/login.html', context)

# ---------------------------------------------------------

# --------Logout------------------------------------------


def logoutPage(request):
    logout(request)
    return redirect('login')

# ---------------------------------------------------------

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
        'form': form,
    }
    return render(request, 'Login_v1/login.html', context)

# ---------------------------------------------------------

# --------Index------------------------------------------


@login_required(login_url='login')
def index(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    chats = Chat.objects.filter(
        Q(user_1=request.user) &
        Q(user_2__username__icontains=q)
    )

    context = {
        'chats': chats,
        'page': 'index'
    }

    return render(request, 'index.html', context)

# ---------------------------------------------------------


@login_required(login_url='login')
def group_index(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    groups = Group.objects.filter(
        Q(users=request.user) &
        Q(name__icontains=q)
    )

    context = {
        'groups': groups,
        'page': 'index'
    }

    return render(request, 'group_index.html', context)

# ---------------------------------------------------------

# --------Room------------------------------------------


@login_required(login_url='login')
def room(request, pk):
    group = Group.objects.get(id=pk)
    chat_messages = group.message_set.all()

    if not request.user in group.users.all():
        messages.error(request, 'No seas cotilla...')
        return redirect('index')

    if request.method == 'POST':
        group.users.remove(request.user)
        return redirect('index')

    context = {
        'group': group,
        'chat_messages': chat_messages
    }
    return render(request, 'chatroom.html', context)

# ---------------------------------------------------------

# --------Contacts------------------------------------------


@login_required(login_url='login')
def contacts(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if request.method == 'POST':

        user_2_id = request.POST.get('contact')
        user_2 = User.objects.get(id=user_2_id)
        user_id_list = sorted([request.user.id, int(user_2_id)])
        try:
            try:
                chat = Chat.objects.get(
                    name=f'{user_id_list[0]}_chat_{user_id_list[1]}', user_2=user_2)
            except:

                chat = Chat.objects.get(
                    name=f'{user_id_list[0]}_chat_{user_id_list[1]}', user_2=request.user.id)
        except:
            chat = Chat.objects.create(
                name=f'{user_id_list[0]}_chat_{user_id_list[1]}',
                user_1=request.user,
                user_2=user_2
            )

            chat_2 = Chat.objects.create(
                name=f'{user_id_list[0]}_chat_{user_id_list[1]}',
                user_1=user_2,
                user_2=request.user
            )

            chat.save()
            chat_2.save()

        return redirect(f'chat/conversation/{chat.name}')

    contacts = User.objects.filter(
        Q(username__icontains=q)
    )

    contacts_len = len(contacts) - 1

    context = {
        'contacts': contacts,
        'number_of_contacts': contacts_len,
    }

    return render(request, 'contacts.html', context)

# ---------------------------------------------------------

# --------Chat------------------------------------------


@login_required(login_url='login')
def chat(request, chat_name):

    try:
        chat = Chat.objects.get(name=chat_name, user_1=request.user)

    except:
        messages.error(request, 'The chat has been deleted...')
        return redirect('index')

    try:
        Notifications.objects.get(chat=chat).delete()
    except:
        pass

    if not request.user == chat.user_1:
        messages.error(request, 'No seas cotilla...')
        return redirect('index')

    if request.method == 'POST':
        wallpaper = request.FILES.get('wallpaper')
        if not wallpaper:
            pass
        else:
            chat.wallpaper = wallpaper
            chat.save()

        return redirect('chat', chat_name)

    user = request.user
    if user.unread_notifications > 0:
        user.unread_notifications -= chat.unread_messages
        if user.unread_notifications < 0:
            user.unread_notifications = 0
        user.save()
    chat.unread_messages = 0
    chat.save()
    context = {
        'chat': chat
    }
    return render(request, 'chat.html', context)

# ---------------------------------------------------------

# --------Create Groups------------------------------------------


@login_required(login_url='login')
def create_group(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

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

    users = User.objects.filter(
        Q(username__icontains=q),
    )
    context = {
        'users': users,
        'form': form,
        'total_users': len(users) - 1,
        'page': 'new_group'
    }
    return render(request, 'group.html', context)

# ---------------------------------------------------------

# --------Delete Chats------------------------------------------


def deleteChats(request, pk):
    try:
        object = Chat.objects.get(id=pk)
        objects = Chat.objects.filter(name=object.name)
    except:
        messages.error(request, 'The chat has been deleted...')
        return redirect('index')

    if request.method == 'POST':
        for obj in objects:
            obj.delete()

        return redirect('index')

    context = {
        'object': object,
        'advise': 'The conversation will be deleted for both',
    }

    return render(request, 'deletePage.html', context)

# ---------------------------------------------------------

# --------Delete Groups------------------------------------------


def deleteGroups(request, pk):
    try:
        object = Group.objects.get(id=pk)
    except:
        messages.error(request, 'The group has been deleted...')
        return redirect('index')

    if request.method == 'POST':
        object.delete()
        return redirect('index')

    context = {
        'object': object,
    }

    return render(request, 'deletePage.html', context)

# ---------------------------------------------------------

# --------Profile------------------------------------------


def profile(request):

    user = request.user

    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        if not bio:
            pass
        else:
            user.bio = bio

        if not profile_picture:
            pass
        else:
            user.avatar = profile_picture
        user.save()

    context = {
        'user': user,
    }

    return render(request, 'profile.html', context)

# ---------------------------------------------------------

# --------Notifications------------------------------------------


def notifications(request):

    user = request.user
    user.unread_notifications = 0
    user.save()

    users_notifications = Notifications.objects.filter(to=user)

    context = {
        'notifications': users_notifications,
        'total_chats_notifications': len(users_notifications),
    }
    return render(request, 'notifications.html', context)

# ---------------------------------------------------------
