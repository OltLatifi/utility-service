# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Token, UsagePermission
from typing import Tuple
from django.db import transaction


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self) -> Tuple[User, Token]:
        with transaction.atomic():
            instance: User = super().save(commit=True)
            token = Token.objects.create(user=instance)
            default_permission: UsagePermission = UsagePermission.objects.get(
                requests_per_second=1
            )

            instance.usage_permission.add(default_permission)
        return (instance, token)
