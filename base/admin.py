from django.contrib import admin
from .models import Topic, Room, Message, User
# from django.contrib.auth.models import User
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
# admin.site.register(User)