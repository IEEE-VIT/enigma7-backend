from rest_framework import generics , mixins
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated , AllowAny
from rest_framework.response import Response
from .models import Question 
from django.shortcuts import get_object_or_404
from .serializers import QuestionSerializer
import json


class Questionview(generics.RetrieveAPIView): #  handling GET request by inherting Mixins for single object 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'

    def get_object(self , *args , **kwargs):
        kwargs = self.kwargs
        q_get = get_object_or_404(Question,id = kwargs['pk'])
        return q_get



