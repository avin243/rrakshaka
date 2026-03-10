from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('success/<int:report_id>/', views.report_success, name='report_success'),
    path('map/', views.public_map, name='public_map'),
]
