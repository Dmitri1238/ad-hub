from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')  # перенаправление после регистрации
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def index(request):
    return HttpResponse("Это страница аккаунтов")