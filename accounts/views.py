from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile created by signal, just update it
            try:
                profile = user.profile
                profile.phone = request.POST.get('phone', '')
                profile.city_ward = request.POST.get('city_ward', '')
                profile.terms_accepted = request.POST.get('terms') == 'on'
                profile.save()
            except Exception as e:
                pass
            
            messages.success(request, 'Account created successfully! You are now logged in.')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
