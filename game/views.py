from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .serializers import QuestionSerializer , HintSerializer
from .models import Question 

from rest_framework import generics , mixins
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated , AllowAny
from rest_framework.response import Response

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



class Answerview(APIView):

    '''
    Post request of form {"answer" : string}

    '''
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self , *args , **kwargs):

        ques_id = self.request.user.question_id  # get the question id in which current user is on 
        user_answer = args[0].data['answer']
        question = get_object_or_404(Question , id = int(ques_id))
        
        if self._isAnswer(question , user_answer):
            return Response({'answer' : True} , status=200)
        return Response({'answer' : False} , status = 200)


    def _isAnswer(self , question , answer):
        if answer in question.answer:
            return True
        return False


class Hintview(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request , *args , **kwargs):
        if self.request.user.points >= 20: # is user has sufficient points (value to change)
            pk = self.kwargs['pk']
            serial = HintSerializer(self.get_object(pk))
            self.request.user.points -= x # deducting points
            return Response(serial.data)
        else:
            resp = {"detail" : "Insufficient points"}
            return Response(resp)
            

    def get_object(self , pk):
        query = get_object_or_404(Question , id = pk)
        return query
        