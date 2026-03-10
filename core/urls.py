from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rewards/', views.rewards, name='rewards'),
    path('reviewer-dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
]
