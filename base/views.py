from django.shortcuts import render, redirect
from .forms import FormRoom, UserUpdateForm, UserRegisterForm
from django.db.models import Q
from .models import Room, Topic, Message,User
from .serializers import RoomSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# rooms = [
#   {'id':1, 'name':"Lets learn Python!"},
#   {'id':2, 'name':"Design with me!"},
#   {'id':3, 'name': 'Frontend developers!'}
# ]

def loginPage(request):
  # page = 'login'
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    # try:
    #   user = User.objects.get(email=email)
    # except:
    #   messages.error(request, "User does not exist")

    user = authenticate(request, email=email, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, "User Email OR Password does not exist")

  # context = {'page': page}
  return render(request, 'login.html')


def LogOut(request):
  logout(request)
  return redirect('home')


def registerUser(request):
  form = UserRegisterForm(request.POST)

  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      return redirect('login')
    else:
      messages.error(request, 'An error occured during registration!')

  return render(request, 'login_register.html', {'form': form})


def userProfile(request, pk):
  user = User.objects.get(id=pk)
  rooms = user.room_set.all()
  room_messages = user.message_set.all()
  topics = Topic.objects.all()
  context = {'user': user,
             'rooms': rooms,
             'room_messages': room_messages,
             'topics': topics}
  return render(request, 'profile.html', context)


@login_required(login_url='login')
def updateUser(request):
  user = request.user
  form = UserUpdateForm(instance=user)

  if request.method == "POST":
    form = UserUpdateForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile', pk=user.id)
  context = {'form': form}
  return render(request, 'update-user.html', context)


def home(request):
  global room_id
  user = User.objects.all()

  q = request.GET.get('q') if request.GET.get('q') != None else ""
  # icontains -> vazifasi q orqali kelgan qiymatlar topic name bitta harifa boslaham togri kelsa chaqiradi
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(description__icontains=q) |
    Q(name__icontains=q) |
    Q(host__username__icontains=q)
  )
  topics = Topic.objects.all()[0:5]
  rooms_count = rooms.count()
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
  return render(request, 'home.html', {
    'rooms': rooms, "topics": topics, "rooms_count": rooms_count, 'room_messages': room_messages
  })


ROOM_ID = 0


def room(request, pk):
  global ROOM_ID
  room = Room.objects.filter(id=pk).first()
  ROOM_ID = room.id
  comments = room.message_set.all()
  participants = room.participants.all()
  if request.method == "POST":
    message = Message.objects.create(
      room=room,
      user=request.user,
      body=request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room', pk=room.id)

  context = {'room': room, 'comments': comments, 'participants': participants}
  return render(request, 'room.html', context)


@login_required(login_url='login')
def createRoom(request):
  topics = Topic.objects.all()
  form = FormRoom()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)

    Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('room_name'),
      description=request.POST.get('room_about')
    )
    return redirect('home')

  # if request.method == "POST":
  #   form = FormRoom(request.POST)
  #   if form.is_valid():
  #     room = form.save(commit=False)
  #     room.host = request.user
  #     room.save()
  #     return redirect('home')
  context = {"form": form, 'topics': topics}
  return render(request, 'room_form.html', context=context)


@login_required(login_url='login')
def updateRoom(request, pk):
  topics = Topic.objects.all()
  room = Room.objects.filter(id=pk).first()
  form = FormRoom(instance=room)
  if request.user != room.host:
    return HttpResponse("You are not allowed here!")

  if request.method == "POST":
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.name = request.POST.get('room_name')
    room.topic = topic
    room.description = request.POST.get('room_about')
    room.save()
    return redirect('home')
    # form = FormRoom(request.POST, instance=room)
    # if form.is_valid():
    #   form.save()
    #   return redirect('home')
  context = {"room": room, "form": form, 'topics': topics}
  return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.user != room.host:
    return HttpResponse("You are not allowed here!")

  if request.method == "POST":
    room.delete()
    return redirect('home')
  return render(request, 'delete.html', {"obj": room})


@login_required(login_url='login')
def deleteMessages(request, pk):
  message = Message.objects.get(id=pk)
  if request.user != message.user:
    return HttpResponse("You are not allowed here!")

  if request.method == "POST":
    message.delete()
    return redirect('room', pk=ROOM_ID)
  return render(request, 'delete.html', {"obj": message.body})


def topicsPage(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ""
  topics = Topic.objects.filter(name__icontains=q)


  return render(request, 'topics.html', {'topics': topics})


def activityPage(request):
  room_messages = Message.objects.filter()
  return render(request, 'activity.html', {'room_messages': room_messages})
