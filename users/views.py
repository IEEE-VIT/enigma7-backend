from rest_framework import generics , mixins
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated , AllowAny
from rest_framework.response import Response
from .models import * 
from django.shortcuts import get_object_or_404
from .serializers import *
import json
from django.shortcuts import render, redirect, get_object_or_404


class User_ViewSet(generics.RetrieveAPIView): #  handling GET request by inherting Mixins for single object 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Users.objects.all()
    serializer_class = User_Serializer
    lookup_field = 'id'

    def get_object(self , *args , **kwargs):
        kwargs = self.kwargs
        user_data = Users.objects.get(id = kwargs['pk'])
        return user_data


class Username_ViewSet(mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = Username_Serialiser
    lookup_field = 'id'
    model = Users

    #to get the queryset

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    #patch username request with partial update

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        serializer = Username_Serialiser(Users, data = request.data, partial = True)
        instance = self.get_object() 
        return self.partial_update(request, *args, **kwargs)

