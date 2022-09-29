from django import forms
from .models import Group

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