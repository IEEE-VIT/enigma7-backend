from django.contrib import admin
from django.urls import path , include
from .views import Questionview

urlpatterns = [
    path('question/<int:pk>', Questionview.as_view()),
]
