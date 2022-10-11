from django import forms
from .models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
            'placeholder': 'Group Name',
            'class' : 'forms-control'
            })
        }

