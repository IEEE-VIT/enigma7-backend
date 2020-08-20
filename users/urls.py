
from django.contrib import admin
from django.urls import path , include
from .views import *
from . import views

urlpatterns = [
    path('<int:pk>', User_ViewSet.as_view()),
    path('username/<int:id>', Username_ViewSet.as_view()),
]