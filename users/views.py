from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import * 
from .serializers import *
from rest_framework.decorators import api_view
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from dj_rest_auth.models import TokenModel
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework import status


class CustomLoginView(LoginView):

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token
            }
            serializer = serializer_class(instance=data,
                                          context=self.get_serializer_context())
        else:
            serializer = serializer_class(instance=self.token,
                                          context=self.get_serializer_context())
        
        if self.user.username == '':
            check = {"username_exists": False}
        else:
            check = {"username_exists": True}
        response = Response({**serializer.data, **check}, status=status.HTTP_200_OK)
        return response        



class GoogleLogin(CustomLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer
    token_model = TokenModel
    callback_url = 'http://127.0.0.1:8000/'
    client_class = OAuth2Client


class InstagramLogin(CustomLoginView):
    permission_classes = ()
    adapter_class = InstagramOAuth2Adapter
    serializer_class = SocialLoginSerializer    
    token_model = TokenModel
    callback_url = 'https://127.0.0.1:8000/'
    client_class = OAuth2Client
    

@api_view(['GET'])
def user_detail_view(request):
    if request.method == 'GET': 
        serializer = Userserializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH'])
def edit_username(request):
    if User.objects.filter(username = request.data['username']).exists():
        return Response({"error":"User with this username already exists"})
    else:
        serializer = UsernameSerializer(
            instance = request.user,
            data = request.data
        )
        serializer.is_valid(raise_exception = True)
        serializer.save() 
        return Response(serializer.data)


