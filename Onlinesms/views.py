from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.



def chatpagehome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Group.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'chatpage.html', context)


def room(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(body__icontains=q)
    )

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room,'rooms': rooms, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
   
    topics = Group.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Group.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        name, created = Group.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=name,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('chatpagehome')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Group.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Group.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('chatpagehome')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('chatpagehome')
    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('chatpagehome')
    return render(request, 'delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Group.objects.filter(name__icontains=q)
    return render(request, 'topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'activity.html', {'room_messages': room_messages})




def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ' You have been logged in successfully.')
            return redirect('home')  # Replace 'dashboard' with your desired URL name
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ' Username or Password did not match. Try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    


    
    
def custom_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            identification_number = form.cleaned_data.get('identification_number')
            password = form.cleaned_data.get('password1')

            # Get the CompanyStaff instance
            staff = genz_database.objects.get(username=username, identification_number=identification_number)

            # Create a new user
            if User.objects.filter(username=username):
                messages.warning(request,"The Username with that ID already exist!")
            else:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user, user_type='genz')
                user.email = staff.email
                user.first_name = staff.first_name
                user.last_name = staff.last_name
                # Save other fields as needed

                user.save()
                login(request, user)
                messages.success(request, 'You account has been created successfully.')
                return redirect('home')
           
        
           
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



def home(request):
    return render(request, 'home.html') 


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('home'))
