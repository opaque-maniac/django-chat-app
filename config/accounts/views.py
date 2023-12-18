from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from . import forms
from . import models

# View for the registration page
def register_view(request):
    if request.method == 'POST':
        form = forms.RegsiterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('accounts:login')
    else:
        context = { 'form': forms.RegsiterForm() }
    return render(request, 'accounts/register.html', context)

# View for the login page
def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('chat:index')
    else:
        context = { 'form': forms.LoginForm() }
    return render(request, 'accounts/login.html', context)

# View for logout
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# View for the profile page
@login_required(login_url='accounts:login')
def profile_view(request):
    profile = models.CustomUser.objects.get(id=request.user.id)
    context = { 'profile': profile }
    return render(request, 'accounts/profile.html')