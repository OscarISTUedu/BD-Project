from django.contrib import admin
from django.urls import path
from BD import views

urlpatterns = [
    path('', views.index, name='home'),
]