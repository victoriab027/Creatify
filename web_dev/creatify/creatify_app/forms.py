from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.safestring import mark_safe

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, "autocomplete": 'off', 'id': "username"}),
        label=mark_safe('Username<br>:::'),
        help_text=':::'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": 'off'}),
        label=mark_safe('Password<br>:::'),
        help_text=':::'
    )