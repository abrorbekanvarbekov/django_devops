from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['name', 'username', 'email', 'password1', 'password2']


class FormRoom(ModelForm):
  class Meta:
    model = Room
    fields =  "__all__"
    exclude = ['host', 'participants']


class UserUpdateForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email','bio', 'avatar', 'email']