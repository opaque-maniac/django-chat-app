from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
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
            return redirect('chat:index')
    else:
        context = { 'form': forms.RegsiterForm() }
    return render(request, 'accounts/register.html', context)

# View for the login page
def login_view(request):
    return auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=forms.LoginForm)(request)

# View for logout
def logout_view(request):
    return auth_views.LogoutView.as_view()(request)

# View for the profile page
@login_required(login_url='accounts:login')
def profile_view(request):
    profile = models.CustomUser.objects.get(id=request.user.id)
    context = { 'profile': profile }
    return render(request, 'accounts/profile.html')