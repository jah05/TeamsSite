from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    city = forms.CharField(max_length=64)
    name = forms.CharField(max_length=64, default="Unnamed")
    bio = forms.TextField(max_length=1024, default='')
    age = forms.IntegerField(default=0)

    class Meta:
        model=User
