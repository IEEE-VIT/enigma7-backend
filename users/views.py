from rest_framework.response import Response
from .models import User
from .serializers import UserOutreachSerializer, UsernameSerializer, Userserializer
from rest_framework.decorators import api_view
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from dj_rest_auth.models import TokenModel
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework import status
from django.conf import settings
from allauth.socialaccount.models import SocialToken
from django.utils import timezone
from datetime import timedelta


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
            }
            serializer = serializer_class(
                instance=data, context=self.get_serializer_context()
            )
        else:
            serializer = serializer_class(
                instance=self.token, context=self.get_serializer_context()
            )

        if self.user.username == '':
            check = {'username_exists': False}
        else:
            check = {'username_exists': True}
        response = Response({**serializer.data, **check}, status=status.HTTP_200_OK)
        return response


class CustomSocialLoginView(CustomLoginView):
    serializer_class = SocialLoginSerializer


class GoogleLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(GoogleLogin, self).post(request, *args, **kwargs)


class InstagramLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = InstagramOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(InstagramLogin, self).post(request, *args, **kwargs)


class CustomAppleOAuth2Adapter(AppleOAuth2Adapter):
    def parse_token(self, data):
        token = SocialToken(
            token=data['access_token'],
        )
        token.token_secret = data.get('refresh_token', '')

        expires_in = data.get(self.expires_in_key)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))

        # `user_data` is a big flat dictionary with the parsed JWT claims
        # access_tokens, and user info from the apple post.
        identity_data = self.get_verified_identity_data(
            data.get('id_token', data.get('access_token'))
        )
        token.user_data = {**data, **identity_data}

        return token


class AppleLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = CustomAppleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(AppleLogin, self).post(request, *args, **kwargs)


@api_view(['GET'])
def user_detail_view(request):
    if request.method == 'GET':

        users = User.objects.order_by('-points', 'user_status__last_answered_ts')

        for counter in range(0, len(users)):
            if users[counter].username == request.user.username:
                rank_dict = {'rank': counter + 1}
                break

        serializer = dict(Userserializer(request.user).data)
        serializer.update(rank_dict)

    return Response(serializer)


@api_view(['PATCH'])
def edit_username(request):
    if User.objects.filter(username=request.data['username']).exists():
        return Response({'error': 'User with this username already exists'})
    else:
        serializer = UsernameSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
def user_outreach(request):
    data = {'user': request.user.id, **request.data}
    serializer = UserOutreachSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def username_exists(request):
    if request.user.username:
        return Response({"username_exists": True})
    else:
        return Response({"username_exists": False})
