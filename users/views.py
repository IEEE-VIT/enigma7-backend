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

class CustomSocialLoginView(CustomLoginView):
    serializer_class = SocialLoginSerializer


class GoogleLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client
    def post(self,request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(GoogleLogin, self).post(request, *args, **kwargs)
    
class InstagramLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = InstagramOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client
    def post(self,request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(InstagramLogin, self).post(request, *args, **kwargs)

@api_view(['GET'])
def user_detail_view(request):
    if request.method == 'GET':

        users = User.objects.order_by('-points')[:25]
        users_list = _split(users)
        
        for counter in range(0,len(users_list)):
            if users_list[counter].username == request.user.username:
                rank_dict = {'rank' : counter + 1}
                break
    
        serializer = dict(Userserializer(request.user).data)
        serializer.update(rank_dict)
        
    return Response(serializer)


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


# Helper functions

def _split(array):
    array = list(array)
    for counter in range(0,len(array)):
        if not counter + 1 == len(array): # rule out , index exceed error
            if array[counter].points == array[counter + 1].points: # if same points
                if array[counter + 1].userstatus.last_answered_ts < array[counter].userstatus.last_answered_ts: # if later object has reached timestamp earlier
                    array[counter + 1] , array[counter] = array[counter] , array[counter + 1] # swapping

    return array