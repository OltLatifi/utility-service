# views.py
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CustomAuthenticationForm, CustomUserCreationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponse('Authenticated')
            else:
                form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


def sign_up_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user, token = form.save()
            login(request, user)
            return HttpResponse(f'Your token is {token.uuid}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/sign_up.html', {'form': form})
