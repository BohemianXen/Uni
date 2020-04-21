from django import forms
from .models import *
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User


class UpdateForm(forms.Form):
    status = forms.HiddenInput()
