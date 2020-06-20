from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.wall_find),
    path('', views.red_to_index),
    
]