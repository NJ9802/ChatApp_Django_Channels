from django import forms
from .models import Group
from django.contrib.auth.models import User

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

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = [
            'username', 'email',
        ]

        # widgets = {
        #     'username':forms.TextInput(
        #         attrs={
        #             'class': 'forms-control',

        #         }
        #     ),

        #     'password': forms.PasswordInput(
        #         attrs={
        #             'class': 'forms-control'
        #         }
        #     )
        # }