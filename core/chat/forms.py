from django import forms
from .models import Group, User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
            
            'class' : 'form-control'
            }),
        }

        labels = {
            'name': 'Group Name'
        }