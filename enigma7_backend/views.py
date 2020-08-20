from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.models import TokenModel
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GoogleLogin(SocialLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    token_model = TokenModel
    callback_url = 'http://127.0.0.1:8000/'
    client_class = OAuth2Client

class InstagramLogin(SocialLoginView):
    permission_classes = ()
    adapter_class = InstagramOAuth2Adapter    
    token_model = TokenModel
    callback_url = 'https://127.0.0.1:8000/'
    client_class = OAuth2Client
    