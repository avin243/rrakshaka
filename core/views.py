from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def rewards(request):
    return render(request, 'core/rewards.html')
