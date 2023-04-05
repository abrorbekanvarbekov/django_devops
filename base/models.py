from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(unique=True, null=True)
  bio = models.TextField(null=True)
  avatar = models.ImageField(null=True, default="avatar.svg")

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

class Topic(models.Model):
  name = models.CharField(max_length=200, default=None)

  class Meta:
    db_table = "Topic"

  def __str__(self):
    return self.name


class Room(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
  name = models.CharField(max_length=200, default=None)
  participants = models.ManyToManyField(User, related_name='participants', blank=True)
  description = models.TextField(default=None)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "Room"
    ordering = ["-created", "-updated"]

  def __str__(self):
    return self.description[:10]

  def desc(self):
    return self.description[:50]


class Message(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
  body = models.TextField(default=None)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "Message"
    ordering = ["-created", "-updated"]
