
from django.urls import path, include
from .views import GoogleLogin, AppleLogin
from . import views
from dj_rest_auth.views import LogoutView
from django.conf.urls import url

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view()),
    url(r'^auth/apple/$', AppleLogin.as_view()),
    path('me/edit/', views.edit_username),
    path('me/', views.user_detail_view),
    path('logout/', LogoutView.as_view()),
    path('outreach/', views.user_outreach),
    path('exists/', views.username_exists),
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
]
