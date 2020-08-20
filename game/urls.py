from django.contrib import admin
from django.urls import path , include
from .views import Questionview , Answerview , Hintview

urlpatterns = [
    path('question/<int:pk>', Questionview.as_view()),
    path('answer', Answerview.as_view()),
    path('hint/<int:pk>', Hintview.as_view()),
]
