from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta():
        model=User
        fields=('username',)#set up fields you want to know from users
