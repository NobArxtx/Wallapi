from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check_proxy),
    path('', views.red_to_index),
    
]