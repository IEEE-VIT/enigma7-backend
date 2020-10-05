from django.urls import path
from .views import *
from . import views
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view()),
    path('me/edit/', views.edit_username),
    path('me/', views.user_detail_view),
    path('logout/',LogoutView.as_view()),
]
