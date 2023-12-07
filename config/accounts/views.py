from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .models import Profile
from . import forms

# View for register
def register(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('accounts:login')
        else:
            print(form.errors)
            context = {'errors': form.errors, 'form': form}
            return render(request, 'accounts/register.html', context)
    else:
        context = {'form': forms.UserForm()}
        return render(request, 'accounts/register.html', context)

# View for login    
def login(request):
    return auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=forms.LoginForm())(request)

def logout(request):
    return auth_views.LogoutView.as_view()(request)

# View for your profile
@login_required
def my_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {'profile': profile}
    return render(request, 'accounts/profile.html', context)

# View for other user's profile
@login_required
def other_profiles(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)
    context = {'profile': profile}
    return render(request, 'accounts/other_profile.html', context)

# View for edit your profile
@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        else:
            print(form.errors)
            context = {'errors': form.errors, 'form': form}
            return render(request, 'accounts/edit_profile.html', context)
    else:
        context = {'form': forms.ProfileForm(instance=profile)}
        return render(request, 'accounts/edit_profile.html', context)
