
from django.contrib import admin
from django.urls import path , include
from .views import *
from . import views

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view()),
    path('auth/instagram/', InstagramLogin.as_view()),
    ]