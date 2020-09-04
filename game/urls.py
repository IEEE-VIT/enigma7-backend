from django.contrib import admin
from django.urls import path , include
from .views import Questionview , Answerview , Hintview

urlpatterns = [
    path('question/', Questionview.as_view()),
    path('answer/', Answerview.as_view()),
    path('hint/', Hintview.as_view()),
]
