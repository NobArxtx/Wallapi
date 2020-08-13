from django.contrib import admin
from django.urls import path , re_path
from . import views

urlpatterns = [
    re_path(r'^search/(?P<q>\w*)/$', views.wall_find),
    path('', views.red_to_index),
    
]
